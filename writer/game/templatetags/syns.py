from django import template
from writer.game.models import Synonims
from django.db.models import Q
from random import sample

register = template.Library()

def syn(v):
    values = v.split('; ')
    general_word_list = []
    unfiltered_word_list = []
    def_list = []
    try:
        for value in values:
            args = Q(title=value)
            word = Synonims.objects.filter(args).first()
            def_list.append(word)
            word_list = word.syns.split(', ')
            unfiltered_word_list += word_list
            exclude_list = []
            if word.used:
                exclude_list = word.used.split(', ')
            word_list.append(word.title)
            res_list = list(set(word_list) - set(exclude_list))
            general_word_list += res_list
        if not general_word_list:
            for word in def_list:
                word.used = None
                word.save()
            general_word_list = unfiltered_word_list
        ret = sample(general_word_list, 1)[0]
        for word in def_list:
            if not word.used:
                word.used = ret
            else:
                word.used = '%s, %s' % (word.used, ret)
            word.save()
    except:
        ret = sample(values, 1)[0]
    return ret

register.filter('syn', syn)


def ch(value):
    words_list = value.split(';')
    return sample(words_list, 1)[0]

register.filter('ch', ch)
