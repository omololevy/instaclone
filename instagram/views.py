from django.http.response import Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from .forms import *
from django.contrib import messages
from .models import Image, Comments, Profile, Follow
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.views import generic 
from cloudinary.forms import cl_init_js_callbacks
from django.views.decorators.csrf import csrf_exempt
from .email import send_welcome_email


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            name=form.cleaned_data['fullname']
            email=form.cleaned_data['email']
           
            send_welcome_email(name,email)

            user = authenticate(username=username, password=password)

            login(request, user)

            return redirect('instagram:home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



def home_page(request):
    current_user = request.user
    posts = Image.objects.all()
   
    user = User.objects.get(username=current_user.username)
    users = User.objects.exclude(username=current_user.username).exclude(is_superuser=True)
    all_users = User. objects.all()
  
    ctx = {
        'posts':posts,
        'user':user,
        'users':users,     
        'all_users':all_users,
        }

    return render(request,'instagram/home_page.html',ctx)

@login_required(login_url='/accounts/login/')
def upload_picture(request):
    current_user = request.user
    user = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = UploadImageModelForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            return redirect('/',username=request.user)
    else:
        form = UploadImageModelForm()
    return render(request,'instagram/upload_picture.html',{'form':form})

@login_required(login_url='/accounts/login/')
def view_post(request,pk):
    post = Image.objects.get(id=pk)
    try:
        comments = Comments.filter_comments_by_post_id(pk)
        print(comments)
        
    except Comments.DoesNotExist:  
        comments = None
    
    ctx = {
        'post':post,
        "comments":comments
        }
    
    return render(request,'instagram/view_post.html',ctx)

@login_required(login_url='/accounts/login/')
def add_comment(request,post_id):
    current_user = request.user
    if request.method == 'POST':
        comment= request.POST.get('comment')
    post = Image.objects.get(id=post_id)
    user_profile = User.objects.get(username=current_user.username)
    Comments.objects.create(
         comment=comment,
         post = post,
         user=user_profile   
        )
    return redirect('instagram:view_post' ,pk=post_id)

@login_required(login_url='/accounts/login/')
def like_post(request,post_id):
  
    post = Image.objects.get(pk=post_id)
    is_liked = False
    user=request.user.profile
    try:
        profile=Profile.objects.get(user=user.user)
        print(profile)

    except Profile.DoesNotExist:
        raise Http404()
    if post.likes.filter(id=user.user.id).exists():
        post.likes.remove(user.user)
        is_liked=False
    else:
        post.likes.add(user.user)
        is_liked=True
    return HttpResponseRedirect(reverse('instagram:home'))


@login_required
def search_results(request):
    if 'search_profile' in request.GET and request.GET["search_profile"]:
        search_term = request.GET.get("search_profile")
        searched_profiles = Profile.search_profile(search_term)
        print(searched_profiles)
        message = f"{search_term}"
        return render(request, 'instagram/search_results.html', {"message":message,"profiles": searched_profiles})
    else:
        message = "You haven't searched for any profile"
    return render(request, 'instagram/search_results.html', {'message': message})

def follow(request,id):
    if request.method == 'GET':
        user_follow=User.objects.get(pk=id)
        follow_user=Follow(follower=request.user, followed=user_follow)
        follow_user.save()
        return redirect('instagram:user_profile' ,username=user_follow.username)
    
def unfollow(request,id):
    if request.method=='GET':
        user_unfollow=User.objects.get(pk=id)
        unfollow_user=Follow.objects.filter(follower=request.user,followed=user_unfollow)
        unfollow_user.delete()
        return redirect('instagram:user_profile' ,username=user_unfollow.username)

def profile(request,username):
    user = User.objects.get(username=username)
    posts = Image.objects.filter(user = user.id)
    follow = Follow.objects.filter(follower_id = user.id)
    profile=Profile.filter_profile_by_id(user.id) 

    ctx = {
        "posts":posts,
        "profile":profile,
        'user':user,
        }  
    return render(request, 'profile/profile.html',ctx)

def user_profile(request,username):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    user_select = User.objects.get(username=username)
    if user_select == user:
        return redirect('instagram:profile', username=request.user.username)
    
    posts = Image.objects.filter(user = user_select.id)
    follow = Follow.objects.filter(follower_id = user_select.id)
    
    profile=Profile.filter_profile_by_id(user_select.id)
      
    followers = Follow.objects.filter(followed=user_select.id)
   
    follow_status = False
    for follower in followers:
        if user.id == follower.follower.id:
            follow_status = True
            break
        else:
            follow_status = False
  
    ctx = {
        "posts": posts,
        "profile": profile,
        "user": user,
        'user_select': user_select,
        'followers': followers,
        'follow_status': follow_status
        }
   
    return render(request, 'instagram/user_profile.html',ctx)

def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user = user)
    form = UpdateUserProfileForm(instance=profile)
    if request.method == "POST":
            form = UpdateUserProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():  
                
                profile = form.save(commit=False)
                profile.save()
                return redirect('instagram:profile' ,username=user.username) 
            
    ctx = {"form":form}
    return render(request, 'profile/update_profile.html', ctx)
    
    
    