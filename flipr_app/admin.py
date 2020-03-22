from django.contrib import admin
from flipr_app.models import CustomUser, PersonalBoard, Card, List, TeamBoard, TeamBoardMember
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(PersonalBoard)
admin.site.register(Card)
admin.site.register(List)
admin.site.register(TeamBoard)
admin.site.register(TeamBoardMember)
