from game.models import Game, Campionat, News, Team, Player
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context
import datetime


def hero_of_the_day(day=datetime.date.today(), campionat=None):
    args = Q(pub_date=day)
    if campionat:
        args &= Q(campionat=campionat)
    game_list = Game.objects.filter(args).all()
    hero = {'player': None, 'points': 0, 'data': None}
    ret = False
    for game in game_list:
        h = game.hero()
        if h and (h['points'] > hero['points']):
            hero = h
            ret = True
    if ret:
        return hero
    return None


def base(request, campionat=None):
    news_args = Q()
    games_args = Q()
    campionat_item = None
    if campionat:
        campionat_item = Campionat.objects.get(slug=campionat)
        news_args &= Q(game__campionat=campionat_item)
        games_args &= Q(campionat=campionat_item)
        try:
            clasament_list = [campionat_item.clasament()]
        except:
            clasament_list = []
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
            try:
                clasament_list.append(campionat.clasament())
            except:
                pass
    hero = hero_of_the_day(day=last_game.pub_date, campionat=campionat_item)
    return render(request, 'index.html',
                  {'news_list': newses, 'campionat_list': campionat_list,
                   'game_list': game_list, 'image_list': image_list,
                   'clasament_list': clasament_list, 'hero': hero})


def news(request, campionat=None, title=None):
    news_item = News.objects.filter(
        game__campionat__slug=campionat,
        slug=title
    ).first()
    campionat_list = Campionat.objects.all()
    clasament_list = []
    try:
        clasament_list = [news_item.game.render_clasament()]
        if news_item.game != news_item.game.campionat.game_set.first():
            clasament_list.append(news_item.game.campionat.clasament())
    except:
        pass
    hero = news_item.game.hero()
    return render(request, 'news.html',
                  {'news_item': news_item, 'campionat_list': campionat_list,
                   'clasament_list': clasament_list, 'hero': hero})


def team(request, campionat=None, team=None):
    team = Team.objects.filter(
        Q(slug=team) & Q(campionat__slug=campionat)
    ).first()
    clasament_list = [team.campionat.clasament()]
    player_list = list(set(list(Player.objects.filter(
        Q(goal__team=team) & Q(goal__auto=False)).all())))
    game_list = Game.objects.filter(
        Q(team1=team) | Q(team2=team)
    ).order_by('-pub_date')
    return render(request, 'team.html', {'team': team,
                                         'clasament_list': clasament_list,
                                         'player_list': player_list,
                                         'game_list': game_list})


def rss(request, campionat=None):
    args = Q()
    article_list = News.objects.filter(
        Q(pub_date__gte=datetime.date.today())
    ).order_by('-pub_date')
    template = get_template('rss.xml')
    return HttpResponse(template.render(Context(locals())),
                        content_type="application/rss+xml")


def sitemap(request):
    team_list = Team.objects.only('slug', 'campionat').all()
    campionat_list = Campionat.objects.only('slug').all()
    news_list = News.objects.only('slug', 'game').order_by('-pub_date')
    pub_date = news_list.first().pub_date

    template = get_template('sitemap.xml')
    return HttpResponse(template.render(Context(locals())), content_type="application/rss+xml")
