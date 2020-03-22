
from django.contrib import admin
from django.urls import path, include
from flipr_app import views
urlpatterns = [
    path('register/', views.Register.as_view(), name="register"),
    path('login/', views.Login.as_view(), name="login"),
    path('personal_boards/', views.PersonalBoardView.as_view(), name="personalBoard"),
    path('team_boards/', views.TeamBoardView.as_view(), name="teamBoard"),
    path('lists/', views.ListView.as_view(), name="lists"),
    path('cards/', views.CardView.as_view(), name="cards"),
    path('attachment/', views.AttachmentView.as_view(), name="attachment"),
    path('downloadAttachment/', views.DownloadAttachMent.as_view(), name="downloadAttachment")
]
