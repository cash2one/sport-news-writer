from game.models import *
from re import split, sub
import urllib2
from BeautifulSoup import BeautifulSoup as Soup
from soupselect import select
import datetime
# import time


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
                print select(row, '.tright')[0].text
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
                        game = Game(campionat=campionat, team1 = home_team, team2 = away_team, goal_team1 = goal_team1, goal_team2 = goal_team2, pub_date=datetime.date.today(), url=score_link)
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
                                    print score_row
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
                                    goal = Goal(author = player, minute=minute, team=team, penalty=penalty, auto=auto, assist=assist)
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

def structure():
    for i in range(0, 3):
        TitleFrase(win_ser=True).save()
        TitleFrase(stop_win_ser=True).save()
        TitleFrase(lose_ser=True).save()
        TitleFrase(stop_lose_ser=True).save()
        TitleFrase(nonlose_ser=True).save()
        TitleFrase(stop_nonlose_ser=True).save()
    for i in range(0, 5):
        TitleFrase(min_total_goals=0, max_total_goals=0).save()
        TitleFrase(min_total_goals=1, max_total_goals=1).save()
        TitleFrase(min_total_goals=2, max_total_goals=6).save()
        TitleFrase(min_total_goals=7, max_total_goals=20).save()
    for i in range(0, 5):
        TitleFrase(min_score_diference=0, max_score_diference=0).save()
        TitleFrase(min_score_diference=1, max_score_diference=1).save()
        TitleFrase(min_score_diference=2, max_score_diference=3).save()
        TitleFrase(min_score_diference=4, max_score_diference=20).save()
    for i in range(0, 5):
        TitleFrase(min_total_goals=2, max_total_goals=4, min_score_diference=1, max_score_diference=2).save()
        TitleFrase(min_total_goals=2, max_total_goals=4, min_score_diference=2, max_score_diference=4).save()
        TitleFrase(min_total_goals=4, max_total_goals=6, min_score_diference=1, max_score_diference=1).save()
        TitleFrase(min_total_goals=4, max_total_goals=6, min_score_diference=3, max_score_diference=6).save()
        TitleFrase(min_total_goals=7, max_total_goals=20, min_score_diference=1, max_score_diference=2).save()
        TitleFrase(min_total_goals=7, max_total_goals=20, min_score_diference=3, max_score_diference=20).save()
    for i in range(0, 5):
        TitleFrase(min_score_diference=0, max_score_diference=0, last_goal_final=True).save()
        TitleFrase(min_score_diference=1, max_score_diference=1, last_goal_final=True).save()
    for i in range(0, 5):
        TitleFrase(triple=True).save()
        TitleFrase(duble=True).save()
        TitleFrase(urcare=True).save()
        TitleFrase(coborire=True).save()

    for i in range(0, 5):
        FirstGoalFrase(min_minute=0, max_minute=15, only=True).save()
        FirstGoalFrase(min_minute=0, max_minute=15, only=False).save()
        FirstGoalFrase(min_minute=16, max_minute=30, only=True).save()
        FirstGoalFrase(min_minute=16, max_minute=30, only=False).save()
        FirstGoalFrase(min_minute=31, max_minute=45, only=True).save()
        FirstGoalFrase(min_minute=31, max_minute=45, only=False).save()
        FirstGoalFrase(min_minute=45, max_minute=60, only=True).save()
        FirstGoalFrase(min_minute=45, max_minute=60, only=False).save()
        FirstGoalFrase(min_minute=61, max_minute=75, only=True).save()
        FirstGoalFrase(min_minute=61, max_minute=75, only=False).save()
        FirstGoalFrase(min_minute=76, max_minute=100, only=True).save()
        FirstGoalFrase(min_minute=76, max_minute=100, only=False).save()

    for i in range(0, 5):
        RegularGoalFrase(equal=True).save()
        RegularGoalFrase(reverse=True).save()
        RegularGoalFrase(only=True).save()
        RegularGoalFrase(duble=True).save()
        RegularGoalFrase(triple=True).save()

    for i in range(0, 5):
        LastGoalFrase(equal=True).save()
        LastGoalFrase(reverse=True).save()
        LastGoalFrase(only=True).save()
        LastGoalFrase(victory=True).save()
        LastGoalFrase(victory=True, reverse=True).save()
        LastGoalFrase(only=True, equal=True).save()
    return 'ok'

