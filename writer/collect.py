# -*- coding: utf-8 -*-

import game.models
from django.db.models import Q
from re import split, sub
import urllib2
from BeautifulSoup import BeautifulSoup as Soup
from soupselect import select
import datetime
from apiclient.discovery import build
from unidecode import unidecode
from urlparse import urlparse
import urllib
from django.core.files import File
from time import sleep
from slugify import slugify


DEVELOPER_KEY = "AIzaSyB0KMU3GZcwr5D-UqN46ZhlnjQLyNQwi20"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_or_create_player(name):
    if not game.models.Player.objects.filter(name=name).count():
        player = game.models.Player(name=name)
        player.save()
    else:
        player = game.models.Player.objects.get(name=name)
    return player


def get_or_create_team(title, campionat):
    if not game.models.Team.objects.filter(title=title).count():
        team = game.models.Team(
            title=title, campionat=campionat, slug=slugify(title)
        )
        team.save()
    else:
        team = game.models.Team.objects.get(title=title)
    return team


def update_game_date(row, campionat):
    """
    When we collecting the datas about games from livescore, we can get
    the date of the game from there. Is usefull when you want to add the
    past games. In this case we collect the games until we rich a row with
    the pub_date info, and update all games in this campionat with the given
    value.

    :param row: the row with info about game date
    :type row: soup
    :param campionat: the campionat instance
    :type campionat: writer.game.models.Campionat
    :returns: True
    :rtype: bool
    """
    if 'row-tall' in row['class']:
        date_struct = select(row, '.tright')
        if date_struct:
            date_string = date_struct[0].text.strip()
            print date_string
            if len(date_string.split(' ')) == 2:
                date_string += ', %d' % datetime.date.today().year
            print date_string
            pub_date = datetime.datetime.strptime(date_string, '%B %d, %Y')
            print pub_date
            game.models.Game.objects.filter(
                Q(campionat=campionat) & Q(pub_date__isnull=True)
            ).update(pub_date=pub_date)
    return


def get_score_link(row):
    """
    Get the link to detailed info about the game.
    If we found a link and the game for this link doesn't exist,
    then we give the link. Else we return False.

    :param row: a soup row
    :type row: Soup
    :returns: a link to detailed info about game
    :rtype: str or bool
    """
    score_link = None
    if select(row, '.sco a'):
        relative_link = select(row, '.sco a')[0]['href']
        score_link = 'http://www.livescore.com%s' % relative_link
    print score_link
    if score_link and not game.models.Game.objects.filter(
        url=score_link
    ).count():
        return score_link
    return False


def create_game(row, campionat, load_date, score_link):
    """
    Is a function for creating a game instance from collected datas.

    :param row: the Soup string from where we collect datas
    :type row: soup
    :param campionat: the campionat instance of future game
    :type campionat: writer.game.models.Campionat
    :param load_date: do we need to give the date of game from row, or we can assume that the event happend today?
    :type load_date: bool
    :param score_link: the link to detailed info about this game
    :type score_link: str
    :returns: a game
    :rtype: writer.game.models.Game
    """
    if 'FT' in select(row, 'div.min')[0].text:
        first_team = select(row, '.ply')[0].text
        home_team = get_or_create_team(first_team, campionat)
        second_team = select(row, '.ply')[1].text
        away_team = get_or_create_team(second_team, campionat)
        score = select(row, '.sco')[0].text
        goal_team1 = split(' - ', score)[0]
        goal_team2 = split(' - ', score)[1]
        g = game.models.Game(
            campionat=campionat, team1=home_team,
            team2=away_team, goal_team1=goal_team1,
            goal_team2=goal_team2, pub_date=None, url=score_link
        )
        if not load_date:
            g.pub_date = datetime.date.today()
        g.save()
        return g
    return False


def get_couches(score_soup, g):
    """
    Find the info about couches of teams in this game

    :param score_soup: the soup with detailed info about the game
    :type score_soup: Soup
    :param g: the game instance
    :type g: writer.game.models.Game
    :returns: True
    :rtype: bool
    """
    couches_and_formulas = select(score_soup, 'div.hidden div.col-offset-1')
    couches = []
    if len(couches_and_formulas) >= 3:
        for couch_name in [
            couches_and_formulas[2].text,
            couches_and_formulas[3].text
        ]:
            if game.models.Couch.objects.filter(name=couch_name).count():
                couch = game.models.Couch.objects.filter(
                    name=couch_name
                ).first()
            else:
                couch = game.models.Couch(name=couch_name)
                couch.save()
            couches.append(couch)
        g.team1.couch_human = couches[0]
        g.team2.couch_human = couches[1]
        g.team1.save()
        g.team2.save()
    return


def get_time(score_row):
    """
    Get the minute when the event was happend. Return the minute if any,
    or False if not.

    :param score_row: a soup string with info about event
    :type score_row: soup
    :returns: a minute when the event was happend or False
    :rtype: int or bool
    """
    minute_row = select(score_row, 'div.min')
    if minute_row:
        minute = int(split("'", minute_row[0].text)[0])
        return minute
    return False


def get_author(score_row, g):
    """
    Get info about the author of event and the affected teams

    :param score_row: the soup string with info about event
    :type score_row: soup
    :param g: the game instance
    :type g: writer.game.models.Game
    :returns: the author player, the author team and the recipient team
    :rtype: touple
    """
    if select(score_row, 'span.name')[0].text != '':
        author = select(score_row, 'span.name')[0].text
        team = g.team1
        recipient = g.team2
    else:
        author = select(score_row, 'span.name')[1].text
        team = g.team2
        recipient = g.team1
    player = get_or_create_player(author)
    return (player, team, recipient)


def create_goal(score_row, g):
    """
    Get the info about goal event and create a Goal instance

    :param score_row: the soap string with info about goal
    :type score_row: soap
    :param g: the game instance
    :type g: writer.game.models.Game
    :returns: the goal instance or False
    :rtype: writer.game.models.Goal or bool
    """
    goal_row = select(score_row, 'span.goal')
    if goal_row:
        minute = get_time(score_row)
        print minute
        (player, team, recipient) = get_author(score_row, g)
        penalty = False
        auto = False
        assist = None
        if '(pen.)' in str(score_row):
            print 'we have a penalty'
            penalty = True
        elif '(o.g.)' in str(score_row):
            print 'autogol!!!!!!!!!'
            auto = True
        elif '(assist)' in str(score_row):
            assist = sub(
                '\(assist\)', '', select(score_row, 'span.assist')[0].text
            ).strip()
            assist = get_or_create_player(assist)
            print 'Assist: ', assist
        goal = game.models.Goal(
            author=player, minute=minute, team=team,
            penalty=penalty, auto=auto, assist=assist,
            recipient=recipient
        )
        goal.save()
        player.goals_in_season += 1
        player.goals_total += 1
        player.save()
        g.goals.add(goal)
        g.save()
        return goal
    return False


def create_carton(score_row, g):
    yellow_card_row = select(score_row, 'span.inc.yellowcard')
    red_card_row = select(score_row, 'span.inc.redcard')
    redyellow_card_row = select(score_row, 'span.inc.redyellowcard')
    if yellow_card_row or red_card_row or redyellow_card_row:
        minute = get_time(score_row)
        (player, team, recipient) = get_author(score_row, g)
        card = game.models.Carton(minute=minute, player=player, team=team)
        if not yellow_card_row:
            card.red = True
            if redyellow_card_row:
                card.cumul = True
        card.save()
        g.cartons.add(card)
        g.save()
        return card
    return False


def collect(campionat, load_date=False):
    url = campionat.url
    soup = Soup(urllib2.urlopen(url))
    row_list = select(soup, '.content > div')
    print row_list, len(row_list)
    row_list.reverse()
    for row in row_list:
        if load_date:
            update_game_date(row, campionat)
        if 'row-gray' in row['class']:
            score_link = get_score_link(row)
            if score_link:
                g = create_game(row, campionat, load_date, score_link)
                if g:
                    score_soup = Soup(urllib2.urlopen(score_link))
                    get_couches(score_soup, g)
                    score_row_list = select(score_soup, 'div.row-gray')
                    for score_row in score_row_list:
                        if not create_goal(score_row, g):
                            create_carton(score_row, g)
                    print g.goal_team1, g.goal_team2
                    news = g.news()
                    news.post_to_facebook()
    return 'ok'


def collect_all():
    for campionat in game.models.Campionat.objects.all():
        collect(campionat)
    return 'ok'


def load_new_videos():
    time_delta = datetime.timedelta(hours=120)
    begin_date = datetime.datetime.now() - time_delta
    for g in game.models.Game.objects.filter(
        Q(pub_date__gte=begin_date) & Q(video__isnull=True)
    ).all():
        try:
            collect_video_game(g=g)
        except:
            pass
    return True


def collect_photo(player=None, team=None, g=None):
    year = datetime.date.today().year
    if player:
        goal = game.models.Goal.objects.filter(
            Q(author=player) & Q(auto=False)
        ).order_by('-id').first()
        q = "%s %s %d" % (player.name, goal.team.title, year)
    elif team:
        q = "%s %d" % (team.title, year)
    elif g:
        q = "%s %s %d" % (g.team1.title, g.team2.title, year)
    cse = build("customsearch", "v1", developerKey=DEVELOPER_KEY)
    res = cse.cse().list(
        q=q,
        imgSize="xxlarge",
        num=10,
        cx='008967187802311874018:z5qkxza9s1k',
        searchType="image"
    ).execute()
    for image in res['items']:
        photo = game.models.Photo(title=image['title'])
        name = urlparse(image['link']).path.split('/')[-1]
        try:
            content = urllib.urlretrieve(image['link'])
        except:
            content = None
        if content:
            photo.image.save(name, File(open(content[0])), save=True)
            if player:
                player.photos.add(photo)
                player.save()
            elif team:
                team.photo.add(photo)
                team.save()
            elif g:
                g.images.add(photo)
                g.save()
            print image['link']
    sleep(1)
    return res


def collect_video_game(g, live=False, test=False, only_video=False):
    black_list = ['UCOIJLZuKMOZB8dsuAyRF-zg', 'UCOjl_Kyky0OHv7ToYpyKiZw',
                  'UCMmVPVb0BwSIOWVeDwlPocQ', 'UC76VPTjEuP011r66am5FhFg',
                  'UC30avO2n6knAFiH2c8e4qiw', 'UCP4A2nemKn_Gmd4ODKQkmvA',
                  'UCZe0ebzwxepnz-AmNxltuFw', 'UCQfA_UR-QfDcyt7F0vLYJ-g',
                  'UCSVkHOXzVRt2ILUMu45cXvA', 'UC3cgAea0Rr9DfTG5Zgmfo2A',
                  'UCUZPb4VLzXFLJomBap2faUA', 'UCXwTR89dy_ohV4ZMoSVcc7A',
                  'UCeXqv6GZCX-jZr-IcDCpBXQ', 'UCmJV9Z99_hfCyM2WyGfOHvA',
                  'UCBFar-sN-5f2JROgLV8WL7w', 'UCgZ17coJyBA37IsG-TvcfOA',
                  'UCQzY_fLOEVc36TDy0FI9MVA', 'UCN9hj6XnMycvcIkr1ppEViQ',
                  'UC8Zq4iGiOnbIGLL5QuHIqTA', 'UChBVxoOjAKedPvqX_4NVgtQ',
                  'UCCs93usjv27jdOzjgRkrNIw', 'UCxvXjfiIHQ2O6saVx_ZFqnw',
                  'UCZRtjNx9fy3kbG2LD_n_3Lg', 'UCQGQbGSSfA-P4UR7VejOFNA',
                  'UCqVINbDs614iiH9HTY5NIEg', 'UCb48BM_JsYnBjBPfmg8AeXA',
                  'UCxyJrhTHuoyXAI4OzBYyiWA', 'UCF47xaMexTCtm7rB3PJ0Rog',
                  'UCcB4_90UmK6UaO46XpZtcHg', 'UCsERJiJi7rMBOgBH2GSJ69w',
                  'UC6jxG2fVl1jztFI7ty3YwtQ', 'UClCNFzsgmgtf4IofCZHtW-Q'
                  ]
    delta = datetime.timedelta(120)
    if live:
        delta = datetime.timedelta(24)
    begin_date = g.pub_date.isoformat() + 'T00:00:00Z'
    end_date = g.pub_date + delta
    end_date = end_date.isoformat() + 'T00:00:00Z'
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    # Call the search.list method to retrieve results matching the specified
    # query term.
    kwargs = {}
    if live:
        kwargs['videoDuration'] = 'long'
        kwargs['q'] = '%s %s' % (g.team1.title, g.team2.title)
        kwargs['eventType'] = 'completed'
    else:
        rezumat = 'Highlights'
        if g.campionat.country == u'România':
            rezumat = 'Rezumat'
        kwargs['q'] = '%s %s %s %d %d' % (
            rezumat, g.team1.title, g.team2.title, g.goal_team1, g.goal_team2
        )
    kwargs['part'] = 'id,snippet'
    kwargs['type'] = 'video'
    kwargs['maxResults'] = 50
    kwargs['order'] = 'date'
    kwargs['publishedAfter'] = begin_date
    kwargs['publishedBefore'] = end_date
    kwargs['videoEmbeddable'] = "true"
    kwargs['videoSyndicated'] = "true"
    search_response = youtube.search().list(**kwargs).execute()

    for search_result in search_response.get("items", []):
        print 'Channel id', search_result['snippet']['channelId']
        title = unidecode(search_result['snippet']['title'])
        match = True
        saved = False
        for word in kwargs['q'].split(' '):
            if word not in title:
                match = False
        if match:
            videoId = search_result['id']['videoId']
            video_response = youtube.videos().list(
                part='id,snippet,player',
                id=videoId
            ).execute()
            video = video_response.get("items", [])[0]
            thumbs = video['snippet']['thumbnails']
            image_url = thumbs['high']['url']
            if not test:
                if not only_video:
                    photo = game.models.Photo(title=title)
                    name = urlparse(image_url).path.split('/')[-1]
                    content = urllib.urlretrieve(image_url)
                    photo.image.save(name, File(open(content[0])), save=True)
                    g.images.add(photo)
                    if g.news_set.count():
                        news = g.news_set.first()
                        news.photo = photo
                        news.save()
                player = video['player']['embedHtml']
                if search_result['snippet']['channelId'] not in black_list:
                    if not live and not saved:
                        g.video = player
                        saved = True
                    elif not saved:
                        g.live = player
                        saved = True
                    g.save()
            else:
                print title
    return True
