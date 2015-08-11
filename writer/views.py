from game.models import Game, Campionat, News, Team, Player
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context
import datetime
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse


def create_breadcrumbs(crumbs):
    """
    This is a function for creating breadcrumbs.

    :param crumbs: a list of locations and names. Something like [('/team/1/', 'Barcelona'), ('/team/1/2/', 'Ronaldinho')]
    :returns: an html formated breadcrumbs
    :rtype: str
    """
    ret = '<a href="/">/</a> &rarr; '
    number_of_elements = len(crumbs) - 1
    for i, element in enumerate(crumbs):
        (url, name) = element
        if i < number_of_elements:
            ret += '<a href="%s">%s</a> ' % (url, name)
            ret += '&rarr; '
        else:
            ret += name
    return ret


def hero_of_the_day(day=datetime.date.today(), campionat=None):
    """
    This function calculate the hero of the day. For each game we can calculate the hero by using the method game.hero().
    By default we think that we are interested in today.

    :param day: a day for calculating hero
    :type day: datetime.date
    :param campionat: the campionat for calculating hero. If is None, then we calculate for all leagues.
    :type campionat: writer.game.models.Campionat
    :returns: a dict with player, the number of points and datas about why we think it's an hero.
    :rtype: dict
    """
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
    crumbs = ''
    news_args = Q(pub_date__lte=datetime.datetime.now())
    games_args = Q(ft=True)
    campionat_item = None
    if campionat:
        campionat_item = get_object_or_404(Campionat, slug=campionat)
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
    if campionat_item:
        crumbs = create_breadcrumbs([
            (None, campionat_item.title)
        ])
    return render(request, 'index.html',
                  {'news_list': newses, 'campionat_list': campionat_list,
                   'game_list': game_list, 'image_list': image_list,
                   'clasament_list': clasament_list, 'hero': hero,
                   'campionat_item': campionat_item, 'crumbs': crumbs})


def news(request, campionat=None, title=None):
    news_item = News.objects.filter(
        game__campionat__slug=campionat,
        slug=title
    ).first()
    if not news_item:
        raise Http404
    campionat_list = Campionat.objects.all()
    clasament_list = []
    try:
        clasament_list = [news_item.game.render_clasament()]
        if news_item.game != news_item.game.campionat.game_set.first():
            clasament_list.append(news_item.game.campionat.clasament())
    except:
        pass
    hero = news_item.game.hero()
    crumbs = create_breadcrumbs([
        (reverse('campionat',
                 kwargs={'campionat': news_item.game.campionat.slug}
                 ), news_item.game.campionat.title),
        (None, news_item.title)
    ])
    other_news_list = News.objects.filter(
        Q(game__campionat=news_item.game.campionat) &
        Q(game__pub_date=news_item.game.pub_date) &
        Q(pub_date__lt=news_item.pub_date)
    ).order_by('-id')
    return render(request, 'news.html',
                  {'news_item': news_item, 'campionat_list': campionat_list,
                   'clasament_list': clasament_list, 'hero': hero,
                   'crumbs': crumbs, 'other_news_list': other_news_list})


def teams(request, campionat=None):
    campionat = get_object_or_404(Campionat, slug=campionat)
    team_list = campionat.team_set.all()
    clasament_list = []
    try:
        clasament_list = [campionat.clasament()]
    except:
        pass
    campionat_list = Campionat.objects.all()
    return render(request, 'teams.html', {'team_list': team_list,
                                          'clasament_list': clasament_list,
                                          'campionat_list': campionat_list})


def team(request, campionat=None, team=None):
    team = Team.objects.filter(
        Q(slug=team) & Q(campionat__slug=campionat)
    ).first()
    if not team:
        raise Http404
    clasament_list = [team.campionat.clasament()]
    player_list = list(set(list(Player.objects.filter(
        Q(goal__team=team) & Q(goal__auto=False)).all())))
    game_list = Game.objects.filter(
        Q(ft=True) &
        (Q(team1=team) | Q(team2=team))
    ).order_by('-pub_date')
    crumbs = create_breadcrumbs([
        (reverse('campionat',
                 kwargs={'campionat': team.campionat.slug}
                 ), team.campionat.title
         ),
        (None, team.title)
    ])
    return render(request, 'team.html', {'team': team,
                                         'clasament_list': clasament_list,
                                         'player_list': player_list,
                                         'game_list': game_list,
                                         'crumbs': crumbs})


def rss(request, campionat=None, team=None):
    args = Q(pub_date__lte=datetime.datetime.now())
    if campionat:
        args &= Q(game__campionat__slug=campionat)
        if team:
            args &= (Q(game__team1__slug=team) | Q(game__team2__slug=team))
    article_list = News.objects.filter(args).order_by('-pub_date')[0:50]
    template = get_template('rss.xml')
    return HttpResponse(template.render(Context(locals())),
                        content_type="application/rss+xml")
