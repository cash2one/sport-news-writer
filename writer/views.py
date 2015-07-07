from game.models import Game, Campionat, News
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context


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
    hero = news.game.hero()
    return render(request, 'news.html',
                  {'news_item': news_item, 'campionat_list': campionat_list,
                   'clasament_list': clasament_list, 'hero': hero})


def rss(request, campionat=None):
    args = Q()
    article_list = News.objects.order_by('-pub_date')[0:30]
    template = get_template('rss.xml')
    return HttpResponse(template.render(Context(locals())),
                        content_type="application/rss+xml")
