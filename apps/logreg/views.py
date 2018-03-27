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
       return redirect('/landing_page')
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
        return redirect('/landing_page')

def landing_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context ={
        'liked_quotes': Post.objects.filter(liked_by = user),
        'unliked_quotes': Post.objects.exclude(liked_by = user),
        'user':User.objects.get(id=request.session['user_id'])
    }
    return render(request,'logreg/quotes.html', context)

def createPost(request):
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
            return redirect('/landing_page')
            isvalid = True

    Post.objects.create(posted_by=user, message=request.POST['desc'], quoted_by = request.POST['quotedBy'])
    return redirect('/landing_page')

def createFavorite(request):
    # add to the db - relationship table
    user_id = request.session['user_id']
    post_id= request.POST['post_id']
    User.objects.get(id=user_id).liked_posts.add(Post.objects.get(id=post_id))
    return redirect('/landing_page')

def removeFavorite(request):
    #delete to the db - relationship table
    user_id = request.session['user_id']
    post_id= request.POST['post_id']
    User.objects.get(id=user_id).liked_posts.remove(Post.objects.get(id=post_id))
    return redirect('/landing_page')

def users(request, id):
    #display the name, count of uploaded quotes and the list of the uploaded quotes
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request,'logreg/users.html',context)

def logout(request):
    request.session.clear()
    return redirect('/')






