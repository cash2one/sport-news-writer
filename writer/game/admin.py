from django.contrib import admin
from models import Photo, Season, Campionat, Player, Couch, Team, Goal, Game
from models import News, Carton
from models import TitleFrase, FirstGoalFrase, RegularGoalFrase, GoalGroupFrase
from models import LastGoalFrase, Conclusion, Synonims, PreviouseGameFrase

# Register your models here.

admin.site.register(Photo)
admin.site.register(Season)
admin.site.register(Campionat)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'goals_total']
admin.site.register(Player, PlayerAdmin)
admin.site.register(Couch)
admin.site.register(Team)
admin.site.register(Carton)
admin.site.register(Game)
admin.site.register(Goal)
class TitleFraseAdmin(admin.ModelAdmin):
    list_display = ('title', 'min_score_diference', 'max_score_diference', 'min_total_goals', 'max_total_goals',
                    'last_goal_final', 'triple', 'duble', 'urcare', 'coborire', 'win_ser', 'stop_win_ser', 'lose_ser', 'stop_lose_ser',
                    'nonlose_ser', 'stop_nonlose_ser')

admin.site.register(TitleFrase, TitleFraseAdmin)
class FirstGoalFraseAdmin(admin.ModelAdmin):
    list_display = ('title', 'min_minute', 'max_minute', 'only')

admin.site.register(PreviouseGameFrase)

admin.site.register(FirstGoalFrase, FirstGoalFraseAdmin)
class RegularGoalFraseAdmin(admin.ModelAdmin):
    list_display = ('title', 'equal', 'reverse', 'only', 'duble', 'triple')

admin.site.register(RegularGoalFrase, RegularGoalFraseAdmin)
admin.site.register(GoalGroupFrase)
admin.site.register(LastGoalFrase)
admin.site.register(Conclusion)
admin.site.register(News)
admin.site.register(Synonims)
