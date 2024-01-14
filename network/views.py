from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import newPostform
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User, newPost, Follow


def index(request):
    post = newPost.objects.all().order_by("id").reverse()
    
    pag = Paginator(post, 10)
    number_page = request.GET.get('page')
    post_page = pag.get_page(number_page)
    
    for i in post:
        print(f"{i.user} posted: {i.content} on {i.date}")
    
    return render(request, "network/index.html", {
        "form": newPostform(),
        "post_page": post_page
    })


def user_profile(request, user):
    user_info = User.objects.get(username=user)
    post = newPost.objects.filter(user=user).order_by("id").reverse()
    
    pag = Paginator(post, 10)
    number_page = request.GET.get('page')
    post_page = pag.get_page(number_page)
    
    for i in post:
        print(f"{i.user} posted: {i.content} on {i.date}")
    
    return render(request, "network/user_profile.html", {
        "post_page": post_page,
        "name": User.username
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def newPost_views(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = newPost(user=user, content=content)
        post.save()
        
        return HttpResponseRedirect(reverse("index"), {
            "form": newPostform()
        })
        
def profile(request, user_id):
    userClicked = User.objects.get(id=user_id) 
    post = newPost.objects.filter(user=userClicked).order_by("id").reverse()
    
    pag = Paginator(post, 10)
    number_page = request.GET.get('page')
    post_page = pag.get_page(number_page)
    
    # for i in post:
    #     print(f"{i.user} posted: {i.content} on {i.date}")
    
    following = Follow.objects.filter(user=userClicked)
    follower = Follow.objects.filter(follower=userClicked)
    currentUser = request.user.id
    verify_follow = follower.filter(user=currentUser)
    if len(verify_follow) == 0:
        isFollow = False
    else:
        isFollow = True
    
    return render(request, "network/profile.html", {
        "form": newPostform(),
        "post_page": post_page,
        "name": userClicked.username,
        "following": following.count(),
        "follower" : follower.count(),
        "isFollow": isFollow,
        "user_profile": userClicked
    })  
    
def follow(request):
    userfollow = request.POST["userfollow"]
    currentUser = User.objects.get(id=request.user.id)
    userFollowData = User.objects.get(username = userfollow)
    f = Follow(user=currentUser, follower=userFollowData)
    f.save()
    user_id = userFollowData.id
    return HttpResponseRedirect(reverse(profile, args=(user_id,)))

def unfollow(request):
    userfollow = request.POST["userfollow"]
    currentUser = User.objects.get(id=request.user.id)
    userFollowData = User.objects.get(username = userfollow)
    f = Follow.objects.get(user=currentUser, follower=userFollowData)
    f.delete()
    user_id = userFollowData.id
    return HttpResponseRedirect(reverse(profile, args=(user_id,)))

def following(request):
    currentUser = User.objects.get(id=request.user.id)
    followPeople = Follow.objects.filter(user=currentUser)
    allPosts = newPost.objects.all().order_by("id").reverse()
    followingPosts = [] 
    
    for post in allPosts:
        for person in followPeople:
            if person.follower == post.user:
                followingPosts.append(post)
    
    pag = Paginator(followingPosts, 10)
    number_page = request.GET.get('page')
    post_page = pag.get_page(number_page)
    
    return render(request, "network/following.html", {
        "post_page": post_page
    })
    
def edit_post(request, post_id):
    print("==================================================================================")
    print(f"post_id: {post_id}")
    if request.method == "POST":
        data = json.loads(request.body)
        print(f"data: {data}")
        editPost = newPost.objects.get(id=post_id)
        print(f"editPost: {editPost}")
        editPost.content = data["content"]
        print(f"editPost.content: {editPost.content}")
        editPost.save()
        return JsonResponse({"message": "Post edited successfully.", "data":data["content"]})
