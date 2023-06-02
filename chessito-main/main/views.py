from django.shortcuts import render, redirect
from .models import Post
from django.views.generic import TemplateView
import main.ChessGame
import json
from django.urls import reverse
from django.http import HttpResponse
from Games.models import GameSession 
from django.http import JsonResponse
from users.models import Profile
from django.contrib.auth.models import User
import numpy as np
"""
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
"""
def home(request):
    games = GameSession.objects.filter(isPrivate=False).filter(isFinished=False)
 
    context = {"games": games}
    return render(request, 'main/lobby_game.html',context)


def about(request):
    return render(request, 'main/about.html', {'title': 'About'})
"""
class PlayGame(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "about.html"
    def get(self, request, format=None, *args, **kwargs):
        data = {"ena":2}
        return Response(data)
"""

def game(request):
    
    if request.method =="GET":
        if request.GET.get("joingame"):
            gamesess = GameSession.objects.get(gameid=request.GET.get("id"))
            if gamesess:
                gamesess.player2 = request.user
                gamesess.save()
                print(reverse('main-play')+f"?id={gamesess.gameid}")
                return redirect(reverse('main-game')+f"?id={gamesess.gameid}")
        elif request.GET.get("create",None):
            context = {}
            return render(request, 'main/create_game.html',context)

        elif request.GET.get("id"):
            gamesess = GameSession.objects.get(gameid=request.GET.get("id"))
            gameid = request.GET.get("id")

            context = {"game":gamesess,"gameid":gameid, "update":True }
            return render(request, 'main/board.html',context)

        
        else: #request.GET.get("join",None):

            games = GameSession.objects.filter(isPrivate=False).filter(isFinished=False)
           
            context = {"games": games}
            return render(request, 'main/lobby_game.html',context)
    elif request.method == "POST":
     
        if request.POST.get("create",None)=="true":
            gamesess = GameSession(player1 = request.user, player2= None, name = request.POST.get("name","My Game!"), isPrivate = request.POST.get("isPrivate",False)=="on" )
            gamesess.save()
        elif request.POST.get("join",None):
        
            gamesess = GameSession.objects.get(gameid=request.POST.get("id"))
            if gamesess:
                gamesess.player2 = request.user
                gamesess.save()
                print(reverse('main-play')+f"?id={gamesess.gameid}")
                return redirect(reverse('main-game')+f"?id={gamesess.gameid}")
        games = GameSession.objects.filter(isPrivate=False).filter(isFinished=False)
        
        context = {"games": games}
      
        return render(request, 'main/lobby_game.html', context)


def send_invite(request):
    
    from onesignal_sdk.client import Client
    
    invited_user = request.GET.get("invited_user")
    user_id = User.objects.get(username=invited_user).profile.onesignal_playerId
    print("EEEEEEEEEEEEEEEEEEE",user_id)
    # For security you should load your app_api_key from enviroment variables
    app_id = "07f7c8ab-fd8e-4109-8667-e76bd06387df"
    app_api_key = 'Y2Y0YjgzMDUtN2ZlZS00NzRjLWEzZDgtODgzNzQzNjdkMjUy'

    # Load OneSignal SDK
    onesignal_client = Client(app_id=app_id, rest_api_key = app_api_key)

    def send_push_notification():
        '''Send a push notification to one or multiple users
        content and headings must be dictionaries {"en": "Message",}
        url is a string
        players_id must be an array
        '''

        notification_body = {
            'contents': {'tr': 'Yeni bildirim', 'en': 'Tienes una invitacion!'},
            'include_player_ids': [user_id],
            'url':f'game/?joingame=1&id={request.GET.get("gameid")}'
        }
        response = onesignal_client.send_notification(notification_body)
        #print(response.body)

        
        # send notification, it will return a response

        return response
    

    # Sample data 
    content = {"en": "Julián, Your Python Developer vacancy has a new candidate. Click for details.", 
                "es": "Julián, tu vacante Python Developer tiene una nueva postulación, haz clic para ver."}
    headings = {"en": "You have a new candidate.", 
                "es": "Tienes un nuevo candidato."}
    player_ids = ["beb59bde-6feb-4351-bed7-b13122b89a73"]
    url = "https://test.myjobstudio.com/vacancy/myjobstudio/bla-bla-bla/56.html"

    send_push_notification()
    return JsonResponse({"mirey":"paila"})
  
def play(request): #cambiar get por post
    if request.is_ajax and request.method =="GET":
     
        gameid = request.GET.get("id")
        user = request.user

        gamesess = GameSession.objects.get(gameid=request.GET.get("id"))

        if gamesess:
            prevmovs = json.loads(gamesess.moves)
         
            
            current_mov =  len(prevmovs)%2 #leer json
            flag = False
            current_user_play = None
            if current_mov==0:

                
                if user == gamesess.player1:
                    flag = True
                current_user_play = gamesess.player1.username
               
            else:
                if user == gamesess.player2:
                    flag = True
                current_user_play = gamesess.player2.username
                
            if flag and request.GET.get("pos1") and request.GET.get("pos2"):

                pos1,pos2 = [int(x) for x in request.GET.get("pos1")],[int(x) for x in request.GET.get("pos2")]
                p2 = main.ChessGame.Player(s=-1)
                p1 = main.ChessGame.Player()

                shogi = main.ChessGame.Chess(p1=p1,p2=p2)
                
                board = shogi.play_moves(prevmovs+[(pos1,pos2)])
                if board is True:
                    gamesess.moves = json.dumps(prevmovs+[(pos1,pos2)])
                    if  not gamesess.winner_player:
                        
                            
                        gamesess.winner_player = gamesess.player1 if (len(prevmovs)+1)%2  else gamesess.player2
                        if gamesess.player1 != gamesess.player2:
                            gamesess.winner_player.win_ctd +=1
                            gamesess.winner_player.save()
                    
                    gamesess.isFinished = True
                    gamesess.save()
                    
                    return JsonResponse({"board":shogi.board_state.tolist(),"current_player":gamesess.winner_player.username+" is the winner"})
                
                elif board is False:
                    board = shogi.play_moves(prevmovs)
                else:
                

                    gamesess.moves = json.dumps(prevmovs+[(pos1,pos2)])
                    gamesess.save()
                    print(board)
            else:
                p2 = main.ChessGame.Player(s=-1)
                p1 = main.ChessGame.Player()

                shogi = main.ChessGame.Chess(p1=p1,p2=p2)
                
                board = shogi.play_moves(prevmovs)

                if board is True:
                    
                    gamesess.isFinished = True
                    if  not gamesess.winner_player:
                        gamesess.winner_player = gamesess.player1 if len(prevmovs)%2  else gamesess.player2
                   
                   
                        if gamesess.player1 != gamesess.player2:
                            gamesess.winner_player.win_ctd +=1
                            gamesess.winner_player.save()                   
                    gamesess.save()
                    return JsonResponse({"board":shogi.board_state.tolist(),"current_player":gamesess.winner_player.username+" is the winner"})
                
                gamesess.moves = json.dumps(prevmovs)
                gamesess.save()
        context = {"board":board.tolist(), "current_player":current_user_play, "current_turn":current_mov}
        return JsonResponse(context)


    elif request.method == "GET":

        context = {
        
        }
    
        return render(request, 'main/lobby_game.html', context)