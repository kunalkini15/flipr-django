from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from flipr_app.models import  CustomUser, PersonalBoard, List, Card, Attachment, TeamBoard, TeamBoardMember

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class Register(APIView):
    def post(self, request):
        print(request.user)
        name = request.data["name"]
        email = request.data["email"]
        password = request.data["password"]

        try:
            user = CustomUser.objects.get(email=email)
            return Response("User already exists", status=status.HTTP_409_CONFLICT)
        except:
            # custom_user = CustomUser.objects.create(name=name, email=email, password=password)
            # custom_user.save()

            user = User.objects.create_user(first_name=name, username=email, email=email, password=password)
            user.save()
        print(name, email, password)
        return Response("User created successfully", status=status.HTTP_201_CREATED)

class Login(APIView):
    def post(self, request):
        print(request.user)


        email = request.data["email"]
        password = request.data["password"]

        try:
            # user = User.objects.get(username=email)
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return Response("User Logged in successfully", status=status.HTTP_200_OK)
            else:
                return Response("Wrong password", status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response("User doesn't exist", status=status.HTTP_404_NOT_FOUND)



class PersonalBoardView(APIView):

    def get(self, request):
        email = request.GET["email"]
        user = User.objects.get(email=email)
        listOfBoards = PersonalBoard.objects.filter(user=user)
        response = []
        for board in listOfBoards:
            new_obj = {
                "name": board.name,
                "id": board.id
            }
            response.append(new_obj)
        return JsonResponse(response, safe=False)

    def post(self, request):

        email = request.data["email"]
        print(email)
        name = request.data["name"]
        user =  User.objects.get(email=email)
        try:
            board = PersonalBoard.objects.create(name=name, user=user)
            response = {
                "name": name,
                "id": board.id
            }

            todoList = List.objects.create(board=board, name="To Do")
            inProgressList = List.objects.create(board=board, name="In Progress")
            completedList = List.objects.create(board=board, name="Completed")
            return JsonResponse(response, safe=False)
        except:
            return JsonResponse("Something went wrong", safe=False)

    def delete(self, request):
        id = request.data["id"]
        board =  PersonalBoard.objects.filter(id=id)
        board.delete()
        return JsonResponse("Successfull", safe=False)

class TeamBoardView(APIView):

    def get(self, request):
        email = request.GET["email"]
        user = User.objects.get(email=email)
        listOfBoards = TeamBoard.objects.filter(owner=user)
        memberBoards = TeamBoardMember.objects.filter(email=email)

        response = []
        for board in listOfBoards:
            new_obj = {
                "name": board.name,
                "id": board.id
            }
            response.append(new_obj)
        for obj in memberBoards:
            new_obj = {
                "name": obj.board.name,
                "id": obj.board.id
            }
            response.append(new_obj)
        return JsonResponse(response, safe=False)

    def post(self, request):

        email = request.data["email"]
        name = request.data["name"]
        members = request.data["members"]

        print(name, members, email)
        user =  User.objects.get(email=email)
        try:
            board = TeamBoard.objects.create(name=name, owner=user)
            response = {
                "name": name,
                "id": board.id
            }

            todoList = List.objects.create(teamBoard=board, name="To Do")
            inProgressList = List.objects.create(teamBoard=board, name="In Progress")
            completedList = List.objects.create(teamBoard=board, name="Completed")

            for i in members:
                TeamBoardMember.objects.create(email=i, board=board)

            return JsonResponse(response, safe=False)
        except:
            return JsonResponse("Something went wrong", safe=False)
        return JsonResponse("Yo", safe=False)

    def delete(self, request):
        id = request.data["id"]
        email = request.data["email"]
        board =  TeamBoard.objects.filter(id=id)
        for i in board:
            if i.owner.email == email:
                print("Hello World")
                board.delete()
                return JsonResponse("Test", safe=False)
        team_board_member = TeamBoardMember.objects.filter(email=email)
        for i in team_board_member:
            print(i.email)
            if i.board.id == id:
                print("YES")
                i.delete()
        return JsonResponse("Successfull", safe=False)


class ListView(APIView):
    def get(self, request):
        id = request.GET["id"]
        personal = request.GET["personal"]
        if personal == True or personal=="true":
            board = PersonalBoard.objects.get(id=id)
            listOfLists = List.objects.filter(board=board)
            lists = []
            for lis in listOfLists:
                new_obj = {
                    "name": lis.name,
                    "id": lis.id
                }
                lists.append(new_obj)

            return JsonResponse(lists, safe=False)
        else:
            board = TeamBoard.objects.get(id=id)
            listOfLists = List.objects.filter(teamBoard=board)
            lists = []
            for lis in listOfLists:
                new_obj = {
                    "name": lis.name,
                    "id": lis.id
                }
                lists.append(new_obj)

            return JsonResponse(lists, safe=False)


    def post(self, request):
        id = request.data["boardId"]
        name = request.data["name"]
        personal = request.data["personal"]

        if personal == True or personal == "true":
            board = PersonalBoard.objects.get(id=id)
            list = List.objects.create(board=board, name=name)
        else:
            board = TeamBoard.objects.get(id=id)
            list = List.objects.create(teamBoard = board, name=name)

        return JsonResponse("Successfull", safe=False)

    def delete(self, request):
        id = request.data["id"]
        list = List.objects.filter(id=id)
        list.delete()
        return JsonResponse("Successfull", safe=False)

class CardView(APIView):

    def get(self, request):
        id = request.GET["id"]

        list = List.objects.get(id=id)
        listOfCards = Card.objects.filter(list_fk=list)
        if len(listOfCards) == 0:
            return JsonResponse([], safe=False)
        cards = []
        for card  in listOfCards:
            new_obj = {
                "id": card.id,
                "name": card.name,
                "description": card.description,
                "completed": card.completed,
                "due_date": card.due_date,
                "due_time": card.due_time,
                "archived": card.archived
            }
            cards.append(new_obj)

        return JsonResponse(cards, safe=False)

    def post(self, request):
        id = request.data["id"]
        name = request.data["name"]
        description = request.data["description"]
        completed = request.data["completed"]
        due_date = request.data["due_date"]
        due_time = request.data["due_time"]

        list_obj = List.objects.get(id=id)

        card = Card.objects.create(list_fk=list_obj, name=name, description=description, completed=completed, due_date=due_date, due_time=due_time)
        return JsonResponse("Successfull", safe=False)

    def delete(self, request):
        id = request.data["id"]
        card = Card.objects.filter(id=id)
        card.delete()
        return JsonResponse("Successfull", safe=False)

    def put(self, request):
        id = request.data["id"]
        print(request.data)
        updateDict = request.data

        del updateDict["id"]
        Card.objects.filter(id=id).update(**updateDict)
        return JsonResponse("Done", safe=False)

class MoveCardView(APIView):
    def post(self, request):
        card_id = request.data["cardId"]
        list_id = request.data["listId"]

        list_obj = List.objects.get(id=list_id)
        card = Card.objects.filter(id = card_id).update(list_fk=list_obj)

        return JsonResponse("Done", safe=False)

class AttachmentView(APIView):
    def post(self, request):
        id = request.data["id"]
        name = (request.data["file"].name)
        file = request.FILES["file"]
        card = Card.objects.get(id=request.data["id"])

        splitName = name.split(".")
        attach = Attachment.objects.create(card=card, name=name, path=None)
        filename = splitName[0] + str(attach.id) + "." + splitName[1]
        default_storage.save(filename, file)
        return JsonResponse("Done", safe=False)

    def get(self, request):
        try:
            print(request.user)
            print(request.data)
        except:
            print("No use")
        id = request.GET["id"]

        card = Card.objects.get(id=id)
        attachments = Attachment.objects.filter(card=card)
        print(len(attachments))
        atts = []
        for attachment in attachments:
            name = attachment.name
            splitName = name.split(".")
            filename = splitName[0] + str(attachment.id) + "." + splitName[1]
            file = default_storage.open(filename)
            new_obj = {
                "id": attachment.id,
                "name": attachment.name,
            }
            atts.append(new_obj)

        return JsonResponse(atts, safe=False)

class DownloadAttachMent(APIView):
    def get(self, request):
        id = request.GET["id"]
        name = request.GET["name"]

        splitName = name.split(".")
        filename = splitName[0] + str(id) + "." + splitName[1]

        file = default_storage.open(filename)
        response = HttpResponse(file, content_type="multipart/form-data")
        response['Content-Disposition'] = "attachment; filename=%s" % name
        return response
