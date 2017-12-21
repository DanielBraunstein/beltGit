# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    if request.session.get('user_id'):
        print "view-index: user is logged-in"
        return redirect('/friends')
    else:
        print "view-index: user is not logged-in"
        return render(request, 'beltApp/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result.id
    print 'view-register: user info validated, redirecting...'
    return redirect('/friends')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result.id
    print 'view-login: user info validated, redirecting...'
    return redirect('/friends')

def logout(request):
    request.session.clear()
    print 'logout complete'
    return redirect('/')

def friends(request):
    print "friends"
    user_context = request.session["user_id"]
    otherUsers = User.objects.exclude(friends = user_context)
    context = {
        'user_context': User.objects.get(id=user_context),
        'otherUsers': otherUsers,
    }
    return render(request, 'beltApp/dashboard.html', context)
    
def like(request, new_friend_id):
    #implemented as a "try" statement to avoid non-logged-in users from friending
    #This also prevents users from friending non-existent users
    #also added a check to prevent a person from friending themselves
    try:
        if request.session["user_id"]==int(new_friend_id):
            print "self friending error"
            return redirect('/')
        else:
            current_user = User.objects.get(id = request.session["user_id"])
            newFriend = User.objects.get(id = new_friend_id)
            current_user.friends.add(newFriend)
            return redirect('/friends')
    except:
        return redirect('/')

def dislike(request, former_friend_id):
    #implemented as a "try" statement to avoid non-logged-in users from defriending
    #This also prevents removing non-existent users as friends, and defriending users who aren't friends with the user
    try:
        current_user = User.objects.get(id = request.session["user_id"])
        former_friend = current_user.friends.get(id = former_friend_id)
        current_user.friends.remove(former_friend)
        return redirect('/friends')
    except:
        return redirect('/')

def userInfo(request, user_id):
    try:
        context= {
            "user":User.objects.get(id = user_id)
        }
        return render(request, 'beltApp/user.html', context)

    except: 
        return redirect('/')
