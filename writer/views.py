from game.models import Game, Goal, Team, Campionat, Player, Photo
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
                            home_team.couch = couches_and_formulas[2].text
                            away_team.couch = couches_and_formulas[3].text
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


def collect_video_game(game, live=False, test=False):
    delta = datetime.timedelta(120)
    begin_date = game.pub_date.isoformat() + 'T00:00:00Z'
    end_date = game.pub_date + delta
    end_date = end_date.isoformat() + 'T00:00:00Z'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    if live:
        q = 'Live'
    else:
        q = 'Highlights'
    q += ' %s %s %d %d' % (game.team1.title, game.team2.title, game.goal_team1, game.goal_team2)
    search_response = youtube.search().list(
        q=q,
        # channelId="UCTv-XvfzLX3i4IGWAm4sbmA",
        part="id,snippet",
        type="video",
        maxResults=50,
        order="date",
        publishedAfter=begin_date,
        publishedBefore=end_date
    ).execute()

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        title = unidecode(search_result['snippet']['title'])
        match = True
        for word in q.split(' '):
            if not word in title:
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
                photo = Photo(title=title)
                name = urlparse(image_url).path.split('/')[-1]
                content = urllib.urlretrieve(image_url)
                photo.image.save(name, File(open(content[0])), save=True)
                player = video['player']['embedHtml']
                game.images.add(photo)
                game.video = player
                game.save()
                break
            else:
                print title
    return 'ok'
