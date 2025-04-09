import uuid
import requests

from zoneinfo import ZoneInfo
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User,Cmd,Posts
from .models import SessionLocal, User
from sqlalchemy.sql import text
from django.shortcuts import redirect
from .common_functions import create_token,get_username_from_token
from django.http import HttpResponse


# Create your views here.
session = SessionLocal()
@api_view(['GET','POST','PATCH'])
def home(request):
    
    method = request.method
    if method == 'GET':
        
        username = request.GET.get("username")
        passwrd = request.GET.get("password")        
        alluser = request.GET.get('all_user')
        following = request.GET.get('following')
        res = dict()
        if not username or not passwrd:
            return render(request,"home.html",{"page":"login","hint":f"Enter valid user name and pass word"})
        if alluser:
            user_details  = session.query(User.username).filter(User.username!=username).all()
            user_details = [ user_detail[0] for user_detail in user_details]
            res.update({"list_of_all_user":user_details})
        result = session.query(User.following,User.password).filter(User.username==username).all()
        if not result:
            return render(request,"home.html",{"page":"login","hint":f"{username} user is not registred click sign up to register"})
        passwrd_db = result[0][1]
        if passwrd != passwrd_db:
            return render(request,"home.html",{"page":"login","hint":f"For user {username} password is wrong"})
        if following:
            res.update({"following":result[0][0]})
        res.update({"status":"success"})

        url = "http://127.0.0.1:8000/quora_clone/log_in/home/questions/"

        list_of_posts_cmds = (requests.request("GET", url, headers={'Authorization': username}, data={})).json()
        
        return render(request,"feed.html",list_of_posts_cmds)

       
    
    elif method == 'POST':
        username = str((request.POST.get("username"))).lower()
        password = request.POST.get("password")
        if not username or not password:
            return render(request,"home.html",{"page":"signup","hint":f"Enter user name and pass word"})
       
        user_details  = session.query(User.username).filter(User.username==username).all()  
        if user_details:
            return render(request,"home.html",{"page":"signup","hint":f"'{username}' user is already exists enter different name"})
        query= f"insert into user_details (username,password) values('{username}','{password}');"
        session.execute(text(query))
        session.commit()
        return render(request,"home.html",{"page":"login","hint":f"Account is created Successfuly enter username and password for log in"})
    
    
    elif method == 'PATCH':
        username = request.headers.get('Authorization')
        # username = get_username_from_token(auth_token)
        following = request.query_params.get('following')
        update_query = f"UPDATE user_details SET following = array_append(following, '{following}') WHERE username = '{username}';"
        session.execute(text(update_query))
        session.commit()
        return Response({"message":f"Following '{following}' user","status": "success"},200)


@api_view(['GET','POST'])
def questions(request):
    method = request.method

    if method == 'GET':
        username = request.headers.get('Authorization')
        following_usernames = session.query(User.following).filter(User.username==username).all()[0][0]
        if not following_usernames:
            return Response({"data":[]})
        posts = session.query(Posts.request_id,Posts.username,Posts.post,Posts.vote,Posts.created_date).filter(Posts.username.in_(following_usernames)).order_by(Posts.created_date.desc()).all()
        col_of_post_cmd={"data":"No posts follows more users"}
        if posts:
            col_of_post_cmd={"data":[]}
            for post in posts:
                post = {
                    "post_request_id":post[0],
                    "user_name":post[1],
                    "post":post[2],
                    "upvote_count":len(post[3]["upvote"]),
                    "you_upvote":True if username in post[3]["upvote"] else False,
                    "post_created_date":post[4].astimezone(ZoneInfo("Asia/Kolkata")).strftime("%d %B %Y %H:%M"),
                    "cmd":"No answer add you answer"
                }
                
                
                post_request_id = post.get('post_request_id')
                cmds = session.query(Cmd.request_id,Cmd.username,Cmd.post,Cmd.vote,Cmd.created_date).filter(Cmd.post_request_id == post_request_id).order_by(Cmd.created_date).all()
                if cmds:
                    col_of_cmds = {"cmd":[]}
                    for cmd in cmds:
                        cmd = {
                            "cmd_request_id":cmd[0],
                            "user_name":cmd[1],
                            "post":cmd[2],
                            "upvote_count":len(cmd[3]["upvote"]),
                            "you_upvote":True if username in cmd[3]["upvote"] else False,
                            "post_created_date":cmd[4].astimezone(ZoneInfo("Asia/Kolkata")).strftime("%d %B %Y %H:%M"),
                        }
                        col_of_cmds["cmd"].append(cmd)
                    post.update(col_of_cmds)
                    


                col_of_post_cmd["data"].append(post)

        return Response(col_of_post_cmd)
    

        
    elif method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        question = request.POST.get("question")
        cmd_request_id = request.POST.get("question_request_id")
        request_id = str(uuid.uuid1())
        if cmd_request_id:
            if question:
                new_post = Cmd(
                    request_id=request_id,
                    username=username,
                    post = question,
                    vote = {"upvote": [], "downvote": []},
                    post_request_id = cmd_request_id
                )
                session.add(new_post)
                session.commit()
        else:
            
            if question:
                new_post = Posts(
                    request_id=request_id,
                    username=username,
                    post = question,
                    vote = {"upvote": [], "downvote": []}
                )
                session.add(new_post)
                session.commit()

       
        return redirect(f"/quora_clone/log_in/home/?username={username}&password={password}")
    
    

@api_view(['POST'])
def votes(request):
    method = request.method
    username = request.POST.get("username")
    password = request.POST.get("password")
    post_type = request.POST.get("post_type")
    request_id = request.POST.get("request_id")
    you_upvote = request.POST.get("you_upvote")
    if method == 'POST':
        if post_type =="question":
            if you_upvote=='False':
                update_query = f"""UPDATE posts SET vote = jsonb_set(vote::jsonb,'{{upvote}}',(vote->'upvote')::jsonb || '"{username}"')WHERE request_id = '{request_id}';"""
                session.execute(text(update_query))
                session.commit()
        elif post_type =="answer":
            if you_upvote=='False':
                update_query = f"""UPDATE cmd SET vote = jsonb_set(vote::jsonb,'{{upvote}}',(vote->'upvote')::jsonb || '"{username}"')WHERE request_id = '{request_id}';"""
                session.execute(text(update_query))
                session.commit()
    return redirect(f"/quora_clone/log_in/home/?username={username}&password={password}")

@api_view(['GET','POST'])
def followers(request):
    method = request.method
   
    
    
    if method == 'GET':
        username = request.GET.get("username")
        password = request.GET.get("password")
        following_usernames = session.query(User.following).filter(User.username==username).all()[0][0]
        
        if following_usernames:
            following_usernames.append(username)
            unfollowing_usernames = session.query(User.username).filter(User.username.notin_(following_usernames)).all()
        else:
            unfollowing_usernames = session.query(User.username).filter(User.username.notin_([username])).all()
        unfollowing_usernames = [unfollow[0] for unfollow in unfollowing_usernames]
        following_usernames.remove(username)
        return render(request,"followers.html",{"following":following_usernames,"unfollowing":unfollowing_usernames})

    elif method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        username_to_follow = request.POST.get("user_to_follow")
        update_query = f"UPDATE user_details SET following = following || '{{{username_to_follow}}}' WHERE username = '{username}';"
        session.execute(text(update_query))
        session.commit()
        return redirect(f"/quora_clone/log_in/home/?username={username}&password={password}")




def login_page(request):
    return render(request,"home.html",{"page":"login"})

def sign_page(request):
    return render(request,"home.html",{"page":"signup"})


def logout(request):
    return render(request,"home.html",{"page":"login"})