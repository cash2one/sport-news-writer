from game.models import Game, Goal, Team, Campionat, Player, Photo, News, Couch
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
from django.shortcuts import render
from django.core.paginator import Paginator
from time import sleep


DEVELOPER_KEY = "AIzaSyB0KMU3GZcwr5D-UqN46ZhlnjQLyNQwi20"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def collect(campionat):
    url = campionat.url
    soup = Soup(urllib2.urlopen(url))
    row_list = select(soup, '.content > div')
    print row_list, len(row_list)
    row_list.reverse()
    i = 0
    for row in row_list:
        if 'row-tall' in row['class']:
            try:
                date_string = select(row, '.tright')[0].text.strip()
                print date_string
                if len(date_string.split(' ')) == 2:
                    date_string += ', 2015'
                print date_string
                pub_date = datetime.datetime.strptime(date_string, '%B %d, %Y')
                print pub_date
                Game.objects.filter(Q(campionat=campionat) & Q(pub_date__isnull=True)).update(pub_date=pub_date)
            except:
                pass
        elif 'row-gray' in row['class']:
            try:
                score_link = 'http://www.livescore.com' + select(row, '.sco a')[0]['href']
                print score_link
                if Game.objects.filter(url=score_link).count() == 0:
                    i += 1
                    print 'we haven\'t this game'
                    if 'FT' in select(row, 'div.min')[0].text:
                        first_team = select(row, '.ply')[0].text
                        if Team.objects.filter(title=first_team).count() == 0:
                            home_team = Team(title=first_team, campionat=campionat)
                            home_team.save()
                        else:
                            home_team = Team.objects.get(title=first_team)
                        second_team = select(row, '.ply')[1].text
                        if Team.objects.filter(title=second_team).count() == 0:
                            away_team = Team(title=second_team, campionat=campionat)
                            away_team.save()
                        else:
                            away_team = Team.objects.get(title=second_team)
                        score = select(row, '.sco')[0].text
                        goal_team1 = split(' - ', score)[0]
                        goal_team2 = split(' - ', score)[1]
                        game = Game(campionat=campionat, team1 = home_team, team2 = away_team, goal_team1 = goal_team1, goal_team2 = goal_team2, pub_date=None, url=score_link)
                        game.save()
                        try:
                            score_link = 'http://www.livescore.com' + select(row, '.sco a')[0]['href']
                            print score_link
                            score_soup = Soup(urllib2.urlopen(score_link))
                            couches_and_formulas = select(score_soup, 'div.hidden div.col-offset-1')
                            couches = []
                            for couch_name in [couches_and_formulas[2].text, couches_and_formulas[3].text]:
                                if Couch.objects.filter(name=couch_name).count():
                                    couch = Couch.objects.filter(name=couch_name).first()
                                else:
                                    couch = Couch(name=couch_name)
                                    couch.save()
                                couches.append(couch)
                            home_team.couch_human = couches[0]
                            away_team.couch_human = couches[1]
                            home_team.save()
                            away_team.save()
                            score_row_list = select(score_soup, 'div.row-gray')
                            for score_row in score_row_list:
                                try:
                                    goal_bool = select(score_row, 'span.goal')[0]
                                    print goal_bool, score_row
                                    minute = int(split("'", select(score_row, 'div.min')[0].text)[0])
                                    print minute
                                    if select(score_row, 'span.name')[0].text != '':
                                        author = select(score_row, 'span.name')[0].text
                                        team = home_team
                                        recipient = away_team
                                    else:
                                        author = select(score_row, 'span.name')[1].text
                                        team = away_team
                                        recipient = home_team
                                    if Player.objects.filter(name=author).count() == 0:
                                        player = Player(name=author)
                                        player.save()
                                    else:
                                        player = Player.objects.get(name=author)
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
                                        assist = sub('\(assist\)', '', select(score_row, 'span.assist')[0].text).strip()
                                        if Player.objects.filter(name=assist).count() == 0:
                                            assist = Player(name=assist)
                                            assist.save()
                                        else:
                                            assist = Player.objects.get(name=assist)
                                        print 'Assist: ', assist
                                    goal = Goal(author = player, minute=minute, team=team, penalty=penalty, auto=auto, assist=assist, recipient=recipient)
                                    goal.save()
                                    player.goals_in_season += 1
                                    player.goals_total += 1
                                    player.save()
                                    game.goals.add(goal)
                                    game.save()
                                except:
                                    pass
                        except:
                            pass
            except:
                pass
    return 'ok'


def collect_all():
    for campionat in Campionat.objects.all():
        collect(campionat)
    return 'ok'



def collect_photo(player=None, team=None):
    if player:
        goal = Goal.objects.filter(
            Q(author=player) & Q(auto=False)
        ).order_by('-id').first()
        q = player.name + ' ' + goal.team.title + ' 2015'
    elif team:
        q = team.title + ' 2015'
    cse = build("customsearch", "v1", developerKey=DEVELOPER_KEY)
    res = cse.cse().list(
        q = q,
        imgSize = "large",
        num = 10,
        cx='008967187802311874018:z5qkxza9s1k',
        searchType = "image"
    ).execute()
    for image in res['items']:
        photo = Photo(title=image['title'])
        name = urlparse(image['link']).path.split('/')[-1]
        content = urllib.urlretrieve(image['link'])
        photo.image.save(name, File(open(content[0])), save=True)
        if player:
            player.photos.add(photo)
            player.save()
        elif team:
            team.photo.add(photo)
            team.save()
        print image['link']
    sleep(1)
    return res


def collect_video_game(game, live=False, test=False, only_video=False):
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
    begin_date = game.pub_date.isoformat() + 'T00:00:00Z'
    end_date = game.pub_date + delta
    end_date = end_date.isoformat() + 'T00:00:00Z'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    kwargs = {}
    if live:
        kwargs['videoDuration'] = 'long'
        kwargs['q'] = '%s %s' % (game.team1.title, game.team2.title)
        kwargs['eventType'] = 'completed'
    else:
        kwargs['q'] = 'Highlights %s %s %d %d' % (game.team1.title, game.team2.title, game.goal_team1, game.goal_team2)
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
                    photo = Photo(title=title)
                    name = urlparse(image_url).path.split('/')[-1]
                    content = urllib.urlretrieve(image_url)
                    photo.image.save(name, File(open(content[0])), save=True)
                    game.images.add(photo)
                player = video['player']['embedHtml']
                if search_result['snippet']['channelId'] not in black_list:
                    if not live and not saved:
                        game.video = player
                        saved = True
                    elif not saved:
                        game.live = player
                        saved = True
                    game.save()
            else:
                print title
    return 'ok'


def base(request, campionat=None):
    news_args = Q()
    games_args = Q()
    if campionat:
        campionat_item = Campionat.objects.get(slug=campionat)
        news_args &= Q(game__campionat=campionat_item)
        games_args &= Q(campionat=campionat_item)
        clasament_list = [campionat_item.clasament()]
    live = request.GET.get('live', False)
    if live:
        news_args &= Q(game__live__isnull=False)
    last_game = Game.objects.filter(games_args).order_by('-pub_date').first()
    games_args &= Q(pub_date=last_game.pub_date)
    game_list = Game.objects.filter(games_args).order_by('-id')
    image_list = []
    for game in game_list:
        for image in game.images.all():
            image_list.append(image)
    news_list = News.objects.filter(news_args).order_by('-pub_date')
    paginator = Paginator(news_list, 10)

    page = request.GET.get('page', 1)
    newses = paginator.page(page)
    campionat_list = Campionat.objects.all()
    if not campionat:
        clasament_list = []
        for campionat in campionat_list:
            clasament_list.append(campionat.clasament())
    return render(request, 'index.html',
                  {'news_list': newses, 'campionat_list': campionat_list,
                   'game_list': game_list, 'image_list': image_list,
                   'clasament_list': clasament_list})


def news(request, campionat=None, title=None):
    news_item = News.objects.filter(game__campionat__slug=campionat, slug=title).first()
    campionat_list = Campionat.objects.all()
    clasament_list = [news_item.game.render_clasament()]
    if news_item.game != news_item.game.campionat.game_set.first():
        clasament_list.append(news_item.game.campionat.clasament())
    return render(request, 'news.html',
                  {'news_item': news_item, 'campionat_list': campionat_list,
                   'clasament_list': clasament_list})


