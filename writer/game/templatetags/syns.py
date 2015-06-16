from django import template
from writer.game.models import Synonims
from django.db.models import Q
from random import sample

register = template.Library()

def syn(value):
    try:
        args = Q(title=value)
        word = Synonims.objects.filter(args).first()
        word_list = word.syns.split(', ')
        word_list.append(word.title)
        return sample(word_list, 1)[0]
    except:
        return value

register.filter('syn', syn)


def ch(value):
    words_list = value.split(';')
    return sample(words_list, 1)[0]

register.filter('ch', ch)
