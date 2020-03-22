from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)

class PersonalBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(null="true")

    def __str__(self):
        return str(self.name)


class TeamBoard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

class TeamBoardMember(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, null=True)
    board = models.ForeignKey("TeamBoard", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.email + " " + self.board.name)

class List(models.Model):
    board = models.ForeignKey('PersonalBoard', on_delete=models.CASCADE, null=True)
    teamBoard = models.ForeignKey('TeamBoard', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)

class Card(models.Model):
    list_fk = models.ForeignKey('List', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length = 50)
    description = models.TextField(null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True)
    due_time = models.TimeField(null=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class Attachment(models.Model):
    card = models.ForeignKey('Card', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    path = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
