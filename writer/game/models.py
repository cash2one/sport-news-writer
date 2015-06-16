from django.db import models
from django.db.models import Q
from django.contrib import admin
from django.template import Context
from django.template import Template
import random
import datetime
from django.template.base import add_to_builtins
import ast
# Create your models here.


def mk_sent(what, verb, when, who, how):
    return "%s %s %s %s %s" % (what, verb, when, who, how)

def ch(value):
    words_list = value.split(';')
    return random.sample(words_list, 1)[0]


def list_authors(authors):
    ret = ''
    for i, author in enumerate(authors):
        goals = 'minutele '
        goals += ', '.join(authors[author])
        if (i != 0) and (i != len(authors) - 1):
            ret += ', '
        if i != len(authors) - 1:
            ret += '%s (%s) ' % (author, goals)
        else:
            ret += 'si %s (%s) ' % (author, goals)
    return ret


class Photo(models.Model):
    title = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='images')

    def __unicode__(self):
        return self.title

admin.site.register(Photo)


class Campionat(models.Model):
    title = models.CharField(max_length=128)
    url = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.title
admin.site.register(Campionat)


class Player(models.Model):
    name = models.CharField(max_length=128)
    goals_in_season = models.IntegerField(default=0)
    goals_total = models.IntegerField(default=0)
    nationality = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.name
admin.site.register(Player)


class Team(models.Model):
    title = models.CharField(max_length=128)
    city = models.CharField(max_length=128, blank=True, null=True)
    couch = models.CharField(max_length=128, blank=True, null=True)
    host = models.NullBooleanField(blank=True, null=True)
    lider = models.NullBooleanField(blank=True, null=True)
    loser = models.NullBooleanField(blank=True, null=True)
    action = models.CharField(max_length=128, blank=True, null=True)
    campionat = models.ForeignKey(Campionat)
    photo = models.ManyToManyField(Photo)

    def __unicode__(self):
        return self.title

    def etape(self, last_id):
        """How many games was this team played until game with the last_id id"""
        count = Game.objects.filter((Q(team1=self) | Q(team2=self)) & Q(id__lte=last_id)).count()
        return count

    def act(self, last_id):
        """
        This method return a qualificative of what happend with team in this game.
        It set the proprety self.action to one of the given expressions.

        :param last_id: the id of game
        :type last_id: int
        """
        game = Game.objects.get(id=last_id)
        if game.winer() == self:
            self.action = ch('a cistigat; a invins; a obtinut o victorie')
        elif game.loser() == self:
            self.action = ch('a fost invinsa; a pierdut; a fost infrinta')
        else:
            self.action = ch('a remizat; a obtinut un egal')
        return 'ok'

    def gramar(self, case):
        """
        This method give a sinonimical expression to the name of the team.

        :param case: the gramatical case (like nominative, genitive, etc.)
        :type case: char, n|g|a
        """
        variants = []
        if case == 'n':
            cei = 'cei de la'
            echipa = 'echipa'
            gazde = 'gazdele'
            oaspeti = 'oaspetii'
            elevii = 'elevii'
            lider = 'liderul'
            loser = 'lanterna rosie'
            variants.append(self.title)
        elif case == 'g':
            cei = 'celor de la'
            echipa = 'echipei'
            gazde = 'gazdelor'
            oaspeti = 'oaspetilor'
            elevii = 'elevilor'
            lider = 'liderului'
            loser = 'lanternei rosii a'
        elif case == 'a':
            cei = 'celor de la'
            echipa = 'echipei'
            gazde = 'gazdelor'
            oaspeti = 'oaspetilor'
            elevii = 'elevilor'
            lider = 'liderului'
            loser = 'lanternei rosii a'
        if self.city:
            variants +=[
                echipa + ' din ' + self.city
            ]
        variants += [
            echipa + ' lui ' + self.couch,
            cei + ' ' + self.title,
            elevii + ' lui ' + self.couch
        ]
        if self.host:
            variants.append(echipa + ' gazda')
            variants.append(gazde)
        else:
            variants.append(echipa + ' oaspete')
            variants.append(oaspeti)
        if self.lider:
            variants.append(lider + ' clasamanetului')
            variants.append(lider + ' campionatului')
        elif self.loser:
            variants.append(loser + ' clasamentului')
            variants.append(loser + ' campionatului')
        return random.sample(variants, 1)[0]

    def n(self):
        """
        The shortcut for self.gramar('n')
        """
        return self.gramar('n')

    def g(self):
        return self.gramar('g')

    def a(self):
        return self.gramar('a')

    def wining_trend(self, last_id=None):
        """
        Identify the wining trend. If the team win a several games consecutivly, it returns a number of wins.

        :param last_id: the id of game
        :type last_id: int
        :returns: the number of wins
        :rtype: int
        """
        args = Q(team1=self)
        args |= Q(team2=self)
        if not last_id:
            last_id = Game.objects.last().id
        args &= Q(id__lte=last_id)
        wins = 0
        for game in Game.objects.filter(args).order_by('-id'):
            if game.winer() == self:
                wins += 1
            else:
                break
        return wins

    def non_lose_trend(self, last_id=None):
        args = Q(team1=self)
        args |= Q(team2=self)
        if not last_id:
            last_id = Game.objects.last().id
        args &= Q(id__lte=last_id)
        wins = 0
        for game in Game.objects.filter(args).order_by('-id'):
            if game.loser() != self:
                wins += 1
            else:
                wins = 0
        return wins

    def partide(self, last_id=None):
        args = Q(team1=self)
        args |= Q(team2=self)
        if not last_id:
            last_id = Game.objects.last().id
        args &= Q(id__lte=last_id)
        return Game.objects.filter(args).count()

    def lose_trend(self, last_id=None):
        args = Q(team1=self)
        args |= Q(team2=self)
        if not last_id:
            last_id = Game.objects.last().id
        args &= Q(id__lte=last_id)
        lose = 0
        for game in Game.objects.filter(args).order_by('-id'):
            if game.loser() == self:
                lose += 1
            else:
                break
        return lose

    def points(self, last_id=None):
        args = Q(team1=self)
        args |= Q(team2=self)
        if not last_id:
            last_id = Game.objects.last().id
        args &= Q(id__lte=last_id)
        points = 0
        for game in Game.objects.filter(args).order_by('id'):
            if game.winer() == self:
                points += 3
            elif game.loser() == self:
                pass
            else:
                points += 1
        return points

    def loc(self, last_id=None):
        loc = -1
        if not last_id:
            last_id = Game.objects.last().id
        args = Q(id__lte=last_id) & Q(campionat=self.campionat)
        game = Game.objects.filter(args).last()
        clasament = game.clasament()
        for i, element in enumerate(clasament):
            if element[1] == self.id:
                loc = i
        return loc + 1

    def loc_prev(self, last_id=None):
        if not last_id:
            last_id = Game.objects.last().id
        if last_id:
            return self.loc(last_id - 1)
        return None

    def vecini(self, last_id=None):
        if not last_id:
            last_id = Game.objects.last().id
        game = Game.objects.get(id=last_id)
        clasament = game.clasament()
        loc = self.loc()
        if loc > 1:
            upper = clasament[loc - 2]
        else:
            upper = None
        if loc != len(clasament):
            lower = clasament[loc + 1]
        else:
            lower = None
        return upper, lower


admin.site.register(Team)


class Goal(models.Model):
    author = models.ForeignKey(Player, blank=True, null=True)
    assist = models.ForeignKey(Player, blank=True, null=True, related_name='assist_goal')
    minute = models.IntegerField()
    team = models.ForeignKey(Team)
    penalty = models.BooleanField(default=False)
    auto = models.BooleanField(default=False)
    recipient = models.ForeignKey(Team, related_name='recipient_team', blank=True, null=True)

    def __unicode__(self):
        return self.author.name

    def what(self):
        v = []
        if self.equal():
            v += [
                '%s care a readus balanta pe tabloul de marcaj' % ch('golul; balonul; reusita; sutul precis'),
                '%s care a readus scorul la egal' % ch('golul; balonul; reusita; sutul precis'),
            ]
        elif self.reverse():
            v += [
                'golul care a intors situatia' % ch('golul; balonul; reusita; sutul precis'),
                'golul care a schimbat balanta de forte pe tabloul de marcaj' % ch('golul; balonul; reusita; sutul precis'),
                'intoarcerea de scor',
                'golul care a rasturnat situatia' % ch('golul; balonul; reusita; sutul precis'),
            ]
        elif self.victory():
            v += [
                'golul victoriei',
                'golul decisiv',
                'golul care a decis rezultatul partidei' % ch('golul; balonul; reusita; sutul precis'),
                'golul care a salvat situatia' % ch('golul; balonul; reusita; sutul precis'),
                'golul care a adus victoria' % ch('golul; balonul; reusita; sutul precis')
            ]
        elif self.auto:
            v += [
                'autogolul',
            ]
        elif self.penalty:
            v += [
                'lovitura de pedeapsa',
                'penalty-ul',
            ]
        else:
            v += [
                'golul',
            ]
        return random.sample(v, 1)[0]

    def how(self):
        v = []
        if self.penalty:
            v += [
                'din penalty',
                'dintr-o lovitura de pedeapsa',
                'dupa executia unei lovituri de pedeapsa'
            ]
        elif self.assist:
            v += [
                'cu concursul lui %s' % self.assist.name,
                'din pasa lui %s' % self.assist.name,
                'fiind asistat de %s' % self.assist.name,
                'ajutat de %s' % self.assist.name,
            ]
        else:
            v += [
                '',
            ]
        return random.sample(v, 1)[0]

    def only(self):
        only = True
        for goal in self.game_set.first().goals.all():
            if (goal.team == self.team) and (goal != self):
                only = False
        return only

    def reverse(self):
        scor_list = self.game_set.first().scor_list()
        order = list(self.game_set.first().goals.all()).index(self)
        if (order > 1) and (((scor_list[order][0] - scor_list[order][1]) * (scor_list[order-2][0] - scor_list[order-2][1])) < 0):
            return True
        return False

    def equal(self):
        scor_list = self.game_set.first().scor_list()
        order = list(self.game_set.first().goals.all()).index(self)
        if scor_list[order][0] == scor_list[order][1]:
            return True
        return False

    def victory(self):
        prev_equal = False
        try:
            prev_last = self.game_set.first().scor_list()[-2]
            if prev_last[0] == prev_last[1]:
                prev_equal = True
        except:
            prev_equal = True

        if (self == self.game_set.first().goals.last()) and prev_equal:
            return True
        return False

    def m(self):
        m = self.minute
        order = list(self.game_set.first().goals.all()).index(self)
        v = []
        if (m < 44) and (m > 30):
            diff = 45 - m
            b_s = 'cu %d minute inainte de' % diff
            v += [
            '%s finalul primei reprize' % b_s,
            '%s a pleca la vestiare' % b_s,
            'cu %d minute pina la pauza' % diff,
            '%s finalul primului mitan' % b_s,
            ]
        elif (m < 88) and (m > 75):
            diff = 90 - m
            b_s = 'cu %d minute inainte de' % diff
            v += [
            '%s finalul reprizei secunde' % b_s,
            '%s a fluierul final' % b_s,
            '%s finalul meciului' % b_s,
            '%s terminarea timpului regulamentar' % b_s,
            ]
        prev_goal_diff = False
        if order > 0:
            prev_goal_diff = m - self.game_set.first().goals.all()[order - 1].minute
        if (order > 0) and (prev_goal_diff < 15) and (prev_goal_diff > 1):
            v += [
                '%d minute mai tirziu' % (m - self.game_set.first().goals.all()[order - 1].minute),
                'dupa %d minute' % (m - self.game_set.first().goals.all()[order - 1].minute),
            ]
        elif prev_goal_diff and (prev_goal_diff < 2):
            v += [
                'citeva clipe mai tirziu',
                'citeva secunde mai tirziu',
                'dupa citeva clipe',
                'dupa citeva secunde',
            ]
        v += [
            'in minutul %d' % m,
        ]
        return random.sample(v, 1)[0]


admin.site.register(Goal)


class Game(models.Model):
    campionat = models.ForeignKey(Campionat, blank=True, null=True)
    team1 = models.ForeignKey(Team, related_name='game_team1')
    team2 = models.ForeignKey(Team, related_name='game_team2')
    goal_team1 = models.IntegerField(default=0)
    goal_team2 = models.IntegerField(default=0)
    pub_date = models.DateField(default=datetime.datetime.today())
    goals = models.ManyToManyField(Goal, blank=True, null=True)
    url = models.CharField(max_length=512, blank=True, null=True)
    classament = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.team1.title + ' ' + str(self.goal_team1) + ':' + str(self.goal_team2) + ' ' + self.team2.title

    ###########
    #         #
    # Methods #
    #         #
    ###########
    def score(self):
        return str(self.goal_team1) + ':' + str(self.goal_team2)

    def class_difference(self):
        return abs(self.team1.points(self.id) - self.team2.points(self.id))

    def lideri(self):
        if (self.team1.loc(self.id) in [1, 2, 3]) and (self.team2.loc(self.id) in [1, 2, 3]):
            return True
        return False

    def surprise(self):
        if self.class_difference() > 10:
            if not self.winer():
                return True
            if self.winer().points() < self.loser().points():
                return True
        return False

    def clasament(self):
        if not self.classament or len(self.classament) < 10:
            clasament = []
            for team in self.campionat.team_set.all():
                points = team.points(self.id)
                clasament.append([points, team.id])
            clasament.sort()
            clasament.reverse()
            self.classament = str(clasament)
            self.save()
        return ast.literal_eval(self.classament)

    def urcare(self):
        urcare = []
        first_id = Game.objects.filter(campionat=self.campionat).first().id
        if self.id > first_id:
            for team in [self.team1, self.team2]:
                if team.loc(self.id) < team.loc_prev(self.id):
                    urcare.append([team, team.loc(self.id), team.points(self.id)])
            if len(urcare) > 0:
                return urcare
        return False

    def coborire(self):
        coborire = []
        first_id = Game.objects.filter(campionat=self.campionat).first().id
        if self.id > first_id:
            for team in [self.team1, self.team2]:
                if team.loc(self.id) > team.loc_prev(self.id):
                    coborire.append([team, team.loc(self.id), team.points(self.id)])
            if len(coborire) > 0:
                return coborire
        return False

    def lupta_loc(self):
        if self.team1.etape(self.id) > 7:
            if self.team1.points(self.id - 1) == self.team2.points(self.id - 1):
                return True
        return False

    def scor_list(self):
        scor_list = []
        scor = [0, 0]
        for goal in self.goals.order_by('minute'):
            if goal.team == self.team1:
                scor[0] += 1
            else:
                scor[1] += 1
            scor_list.append([scor[0], scor[1]])
        return scor_list

    def intoarcere(self):
        scor_list = self.scor_list()
        if len(scor_list) > 2:
            for i in range(2, len(scor_list)):
                if ((scor_list[i][0] - scor_list[i][1]) * (scor_list[i-2][0] - scor_list[i-2][1])) < 0:
                    return True
        return False

    def duble(self):
        duble = []
        for goal in self.goals.all():
            if self.goals.filter(author=goal.author).exclude(id=goal.id).count() == 1:
                duble.append(goal.author)
        return list(set(duble))

    def triple(self):
        triple = []
        for goal in self.goals.all():
            if self.goals.filter(author=goal.author).exclude(id=goal.id).count() == 2:
                triple.append(goal.author)
        return list(set(triple))

    def winer(self):
        if self.goal_team1 > self.goal_team2:
            return self.team1
        elif self.goal_team2 > self.goal_team1:
            return self.team2
        else:
            return None

    def loser(self):
        if self.goal_team1 > self.goal_team2:
            return self.team2
        elif self.goal_team2 > self.goal_team1:
            return self.team1
        else:
            return None

    def score_diference(self):
        return abs(self.goal_team1 - self.goal_team2)

    def total_goals(self):
        return self.goal_team1 + self.goal_team2

    def only(self):
        if self.total_goals() == 1:
            return True
        return False

    def last_goal_final(self):
        """This method tell us if the last goal was on final of the game and was decisive for the result"""
        last_goal = self.goals.last()
        if last_goal and (last_goal.minute > 80) and (last_goal.victory() or last_goal.equal()):
            return True
        return False

    def goals_set(self):
        goals = []
        if self.goals.count():
            group = []
            for goal in self.goals.all():
                if not group:
                    team = goal.team
                if team == goal.team:
                    group.append(goal)
                else:
                    goals.append(group)
                    group = [goal]
                    team = goal.team
            goals.append(group)
        return goals

    #############
    # Templates #
    #############
    def title_frase(self):
        first_id = Game.objects.filter(campionat=self.campionat).first().id
        not_null = Q(title__isnull=False)
        diff = Q(min_score_diference__lte=self.score_diference()) & Q(max_score_diference__gte=self.score_diference())
        diff_null = Q(min_score_diference__isnull=True) & Q(max_score_diference__isnull=True)
        total = Q(min_total_goals__lte=self.total_goals()) & Q(max_total_goals__gte=self.total_goals())
        total_null = Q(max_total_goals__isnull=True, min_total_goals__isnull=True)
        last_final = Q(last_goal_final=self.last_goal_final())

        diff_set = diff & total_null & last_final
        total_set = total & diff_null
        goal_set = diff & total
        sets = [diff_set, total_set, goal_set]

        wins = False
        loses = False
        if self.winer():
            wins = self.winer().wining_trend(self.id)
            if self.winer().wining_trend(self.id) >= 4:
                print '__________________', "We have wining trend!!!"
                win_set = Q(win_ser=True)
                sets = [win_set]
            if self.id > first_id + 39:
                if self.winer().loc(self.id) == 1:
                    sets.append(Q(with_champion=True))
        if self.loser():
            loses = self.loser().lose_trend(self.id)
            if self.loser().lose_trend(self.id) >= 3:
                print '_________________', "we have losing trend :((((", self.loser().lose_trend(self.id)
                lose_set = Q(lose_ser=True)
                sets = [lose_set]
            if self.id > first_id + 39:
                if self.loser().loc_prev(self.id) == 1:
                    sets.append(Q(with_champion=False))

        for i, args in enumerate(sets):
            if i == 0:
                res = TitleFrase.objects.filter(args).filter(not_null).all()
            else:
                res |= TitleFrase.objects.filter(args).filter(not_null).all()
        tpl_string = random.sample(res, 1)[0].title
        tpl = Template(tpl_string)
        return tpl.render(Context({'game': self, 'wins': wins, 'loses': loses}))

    def first_goal_frase(self):
        args = Q()
        args &= Q(only=self.only())
        args &= Q(min_minute__lte=self.goals.all()[0].minute)
        args &= Q(max_minute__gte=self.goals.all()[0].minute)
        args &= Q(title__isnull=False)
        tpl = Template(random.sample(FirstGoalFrase.objects.filter(args).all(), 1)[0].title)
        return tpl.render(Context({'game': self,}))

    def regular_goal_frase(self, goal):
        args = Q()
        args &= Q(only=goal.only())
        args &= Q(reverse=goal.reverse())
        args &= Q(equal=goal.equal())
        args &= Q(duble=False)
        args &= Q(triple=False)
        tpl = Template(random.sample(RegularGoalFrase.objects.filter(args).all(), 1)[0].title)
        return tpl.render(Context({'goal': goal,}))

    def last_goal_frase(self):
        last_goal = self.goals.last()
        scor_list = self.scor_list()
        pre_last_scor = scor_list[len(scor_list) - 2]
        args = Q()
        only = False
        if ((last_goal.team == self.team1) and (self.goal_team1 == 1)) or ((last_goal.team == self.team2) and (self.goal_team2 == 1)):
            only = True
        equal = (self.goal_team1 == self.goal_team2)
        victory = (pre_last_scor[0] == pre_last_scor[1])
        reverse = False
        if (len(scor_list) > 3) and (((scor_list[-1][0] - scor_list[-1][1]) * (scor_list[-2][0] - scor_list[-2][1])) < 0):
            reverse = True
        args &= Q(reverse=reverse)
        args &= Q(only=only)
        args &= Q(equal=equal)
        args &= Q(victory=victory)
        args &= Q(title__isnull=False)
        print self, only, self.intoarcere(), equal, victory
        tpl = Template(random.sample(LastGoalFrase.objects.filter(args).all(), 1)[0].title)
        return tpl.render(Context({'game': self, 'goal': last_goal}))

    def conclusion(self):
        args = Q()
        args &= Q(urcare=(self.urcare() is not False))
        args &= Q(coborire=(self.coborire() is not False))
        tpl = Template(random.sample(Conclusion.objects.filter(args).all(), 1)[0].title)
        var = {
            'game': self,
            'loc1': self.team1.loc(self.id), 'loc2': self.team2.loc(self.id),
            'puncte1': self.team1.points(self.id), 'puncte2': self.team2.points(self.id)
        }
        coborire = self.coborire()
        urcare = self.urcare()
        if urcare:
            var['urc_team'] = urcare[0][0]
            var['urc_loc'] = urcare[0][1]
            var['urc_points'] = urcare[0][2]
        if coborire:
            var['cob_team'] = coborire[0][0]
            var['cob_loc'] = coborire[0][1]
            var['cob_points'] = coborire[0][2]
        return tpl.render(Context(var))

    ###############
    # Making news #
    ###############
    def start(self):
        self.team1.host = True
        for team in [self.team1, self.team2]:
            if team.etape(self.id) > 7:
                if team.loc(self.id - 1) == 1:
                    team.lider = True
                elif team.loc(self.id - 1) == len(self.clasament()):
                    team.loser = True
            team.act(last_id=self.id)
            team.save()

    def stop(self):
        for team in [self.team1, self.team2]:
            team.host = False
            team.lider = False
            team.loser = False
            team.action = ''
            team.save()

    def news(self):
        self.start()
        title = self.title_frase()
        begin_frase = self.title_frase()
        while begin_frase == title:
            begin_frase = self.title_frase()
        if self.lupta_loc():
            begin_frase += ' In aceasta seara cele doua echipe au luptat pentru dreptul de a ocupa locul ' + str(max(self.team1.loc(self.id), self.team2.loc(self.id))) + '. '
        first_goal_frase = ''
        if self.goals.count() > 0:
            first_goal_frase = self.first_goal_frase()
        reg_goals = ''
        if self.goals.count() > 2:
            for i, group in enumerate(self.goals_set()):
                if i == 0:
                    group.pop(0)
                if i == len(self.goals_set()) - 1:
                    group = group[:-1]
                if len(group) > 1:
                    authors = {}
                    for goal in group:
                        cg = authors.get(goal.author.name, [])
                        authors[goal.author.name] = cg + [str(goal.minute)]
                    goals = list_authors(authors)
                    if i == 0:
                        reg_goals += ' Urmeaza golurile lui %s trimise in aceeasi poarta.' % goals
                    else:
                        reg_goals += ' %s a ripostat prin reusitele lui %s.' % (group[0].team.n(), goals)
                elif len(group) == 1:
                    try:
                        reg_goals += ' %s' % self.regular_goal_frase(group[0])
                    except:
                        pass
        last_goal_frase = ''
        if self.goals.count() > 1:
            last_goal_frase = self.last_goal_frase()
        conclusion = self.conclusion()
        self.stop()
        return title + '\n' + begin_frase + '. ' + first_goal_frase + '\n' + reg_goals + '\n' + last_goal_frase + '\n' + conclusion + '\n'

admin.site.register(Game)

class TitleFrase(models.Model):
    title = models.TextField(blank=True, null=True)
    min_score_diference = models.IntegerField(blank=True, null=True)
    max_score_diference = models.IntegerField(blank=True, null=True)
    min_total_goals = models.IntegerField(blank=True, null=True)
    max_total_goals = models.IntegerField(blank=True, null=True)
    last_goal_final = models.BooleanField(default=False)
    triple = models.BooleanField(default=False)
    duble = models.BooleanField(default=False)
    urcare = models.BooleanField(default=False)
    coborire = models.BooleanField(default=False)
    win_ser = models.BooleanField(default=False)
    stop_win_ser = models.BooleanField(default=False)
    lose_ser = models.BooleanField(default=False)
    stop_lose_ser = models.BooleanField(default=False)
    nonlose_ser = models.BooleanField(default=False)
    stop_nonlose_ser = models.BooleanField(default=False)
    with_champion = models.NullBooleanField(default=None)

    def __unicode__(self):
        ret = ''
        if self.title:
            ret += self.title
        ret += '. Score diff: ' + str(self.min_score_diference) + ' - ' + str(self.max_score_diference) + '. Total: ' + str(self.min_total_goals) + ' - ' + str(self.max_total_goals)
        return ret

class TitleFraseAdmin(admin.ModelAdmin):
    list_display = ('title', 'min_score_diference', 'max_score_diference', 'min_total_goals', 'max_total_goals',
                    'last_goal_final', 'triple', 'duble', 'urcare', 'coborire', 'win_ser', 'stop_win_ser', 'lose_ser', 'stop_lose_ser',
                    'nonlose_ser', 'stop_nonlose_ser')
admin.site.register(TitleFrase, TitleFraseAdmin)

class FirstGoalFrase(models.Model):
    title = models.TextField(blank=True, null=True)
    min_minute = models.IntegerField(blank=True, null=True)
    max_minute = models.IntegerField(blank=True, null=True)
    only = models.BooleanField(default=False)
    def __unicode__(self):
        ret = ''
        if self.title:
            ret += self.title + '. '
        ret += str(self.min_minute) + ' - ' + str(self.max_minute)
        return ret
class FirstGoalFraseAdmin(admin.ModelAdmin):
    list_display = ('title', 'min_minute', 'max_minute', 'only')
admin.site.register(FirstGoalFrase, FirstGoalFraseAdmin)

class RegularGoalFrase(models.Model):
    title = models.TextField(blank=True, null=True)
    equal = models.BooleanField(default=False)
    reverse = models.BooleanField(default=False)
    only = models.BooleanField(default=False)
    duble = models.BooleanField(default=False)
    triple = models.BooleanField(default=False)
    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return ''
class RegularGoalFraseAdmin(admin.ModelAdmin):
    list_display = ('title', 'equal', 'reverse', 'only', 'duble', 'triple')
admin.site.register(RegularGoalFrase, RegularGoalFraseAdmin)

class LastGoalFrase(models.Model):
    title = models.TextField(blank=True, null=True)
    equal = models.BooleanField(default=False)
    reverse = models.BooleanField(default=False)
    only = models.BooleanField(default=False)
    victory = models.BooleanField(default=False)
    def __unicode__(self):
        ret = ''
        if self.title:
            ret += self.title
        else:
            ret = 'None'
        return ret
admin.site.register(LastGoalFrase)

class Conclusion(models.Model):
    title = models.TextField(blank=True, null=True)
    urcare = models.BooleanField(default=False)
    coborire = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title
admin.site.register(Conclusion)

class Synonims(models.Model):
    title = models.CharField(max_length=128)
    syns = models.TextField()
    def __unicode__(self):
        return self.title
admin.site.register(Synonims)
add_to_builtins('writer.game.templatetags.syns')
