from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import User, Post, UserManager
from django.core.urlresolvers import reverse
import bcrypt
# Create your views here.

def index(request):
    return render(request, 'logreg/index.html')

def registration(request):
    response = User.objects.validate_register(request.POST)
    if response['status'] == True:
       request.session['user_id'] = response['user_id']
       return redirect('/quotes')
    else: 
        for error in response['errors']:
            messages.error(request, error, extra_tags="registerError")
        return redirect('/')

def login(request):
        result = User.objects.validate_login(request.POST)
        if type(result) == list:
            for item in result:
                messages.error(request, item, extra_tags="loginError")
            return redirect('/')
        request.session['user_id'] = result.id
        messages.success(request, 'Successfully logged in!')
        return redirect('/quotes')

def quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context ={
        'all_favorites': User.objects.get(id=request.session['user_id']).liked_posts.all(),
        'all_user' : User.objects.all().order_by("-created_at"),
        'user':User.objects.get(id=request.session['user_id'])
    }
    return render(request,'logreg/quotes.html', context)

def addQuote(request):
    user = User.objects.get(id=request.session['user_id'])
    error = []
    isvalid = False

    #validation prior to submit
    if len(request.POST['quotedBy']) < 3:
        error.append("Quoted by should contain more than 3 characters")
    if len(request.POST['desc']) < 10:
        error.append("Quotes should not be less than 10 characters")
        for item in error:
            messages.error(request, item, extra_tags ="quoteError")
            return redirect('/quotes')
            isvalid = True

    Post.objects.create(posted_by=user, message=request.POST['desc'], quoted_by = request.POST['quotedBy'])
    return redirect('/quotes')

def addFavorite(request):
    # add to the db - relationship table
    request.session['user_post'] = request.POST['post_id']
    User.objects.get(id=request.session['user_id']).liked_posts.add(Post.objects.get(id=request.session['user_post']))
    return redirect('/quotes')

def delFavorite(request):
    #delete to the db - relationship table
    User.objects.get(id=request.session['user_id']).liked_posts.remove(Post.objects.get(id=request.POST['fav_id']))
    return redirect('/quotes')

def showUserPost(request):
    # get the name who uploaded the quote/s and it's post_id to be displayed in the users page
    request.session['user_name'] = request.POST['show_user']
    request.session['user_post'] = request.POST['post_id']
    return redirect ('/users')

def users(request):
    #display the name, count of uploaded quotes and the list of the uploaded quotes
    context = {
        'user': User.objects.get(name=request.session['user_name']).uploaded_quotes.all()
    }
    return render(request,'logreg/users.html',context)

def logout(request):
    request.session.clear()
    return redirect('/')






