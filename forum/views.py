from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Forum, Comment, Notification
from django.db import transaction
from django.core.paginator import Paginator
from user_auth.models import Profile, Level
from .forms import *
from base.models import Blog, Images
from django.contrib import messages as mg
from django.db.models import Q
from django.shortcuts import get_object_or_404


# Create your views here.
from .util import leader, checkDate, UserNotification


# Checking and keeping track of pages
pages = []


@login_required(login_url='login')
def dashboard(request, pk):
    user_profile = get_object_or_404(Profile, id=pk)
    user_posts = Forum.objects.all().filter(author=user_profile.user, owner=None)
    notify = UserNotification(request.user)
    
    referer = request.META.get('HTTP_REFERER')
    pages.append(referer)

    total_comments = 0
    total_likes = 0

    following = [follow for follow in Profile.objects.all() if user_profile.user in follow.followers.all()]
    num_following = len(following)

    for post in user_posts:
        total_comments += int(post.comment_count)
        total_likes += post.likes.all().count()
    


    context = {
        'user_profile': user_profile,
        'user_post': user_posts,
        'num_following': num_following,
        'following': following,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'date': checkDate(),
        'my_notification': notify.myNotifiction()
    }
    return render(request, 'forum/author.html', context)


def edit_profile(request, pk):
    user_profile = get_object_or_404(Profile, id=pk)
    user = request.user
    error_msg = ''
    notify = UserNotification(request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        level = request.POST.get('level')
        username = request.POST.get('username')
        tiktok = request.POST.get('tiktok')


        tiktok = tiktok.strip()

        if tiktok.startswith('@'):
            tiktok = tiktok
        else: tiktok = f'@{tiktok}' 

        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            user.first_name = first_name
            user.last_name = last_name
            user.level = get_object_or_404(Level, id=level)
            user.username = username
            user.save()

            profile = form.save(commit=False)
            profile.tiktok = tiktok
            profile.save()
            return redirect('dashboard', user_profile.id)
        else:
            errors = form.errors.get_json_data(escape_html=True)
            for error in errors:
                error_msg = errors[error][0]['message']

            mg.error(request, error_msg)


    context = {
        'user_profile': user_profile,
        'my_notification': notify.myNotifiction()
    }
    return render(request, 'forum/dashboard-setting.html', context)


def follow(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    notify = UserNotification(request.user)

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        return redirect('dashboard', profile.id)
    else:
        profile.followers.add(request.user)
        notify.follow_notify(receiver=profile.user, status='follow')
        return redirect('dashboard', profile.id)


@login_required(login_url='login')
def forum(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    forum = Forum.objects.filter(
        Q(title__icontains=q)|
        Q(author__first_name__icontains=q) |
        Q(author__username__icontains=q) |
        Q(description__icontains=q) |
        Q(author__last_name__icontains=q) 
    )

    notify = UserNotification(request.user)

    referer = request.META.get('HTTP_REFERER')
    pages.append(referer)

    paginator = Paginator(forum, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'forum': forum,
        'page_obj': page_obj,
        'leaderboard': leader(),
        'date': checkDate(),
        'my_notification': notify.myNotifiction()
    }
    return render(request, 'forum/forum.html', context)



@login_required(login_url='login')
def edit_forum(request, pk):
    forum = get_object_or_404(Forum, id=pk)
    form = ForumForm(instance=forum)
    edit = True
    notify = UserNotification(request.user)
    referer = request.META.get('HTTP_REFERER')
    pages.append(referer)
    other_forum = [x for x in Forum.objects.all().filter(owner=None)[:5] if x != forum]

    if request.method == 'POST':
        form = ForumForm(request.POST, instance=forum)

        if form.is_valid(): 
            form.save()
            return redirect(f'{pages[-2]}')

    context = {
        'title': forum.title,
        'description': forum.description,
        'edit': edit,
        'form': form,
        'forum': other_forum,
        'my_notification': notify.myNotifiction()
    }
    return render(request, 'forum/forum-form.html', context)

@login_required(login_url='login')
def forum_detail(request, pk):
    forum = get_object_or_404(Forum, id=pk)
    forum_comment = forum.comment_set.all()
    notify = UserNotification(request.user)

    # TRACING THE VISTED PAGES 
    pages.append(request.META.get('HTTP_REFERER'))

    # Checking and increasing the number of views
    if request.user not in forum.views.all():
        forum.views.add(request.user)

    other_forum = [x for x in Forum.objects.all().filter(owner=None)[:5] if x != forum]

    if request.method == 'POST':
        comment = request.POST.get('comment')

        with transaction.atomic():
            Comment.objects.create(
                user=request.user,
                post=forum,
                comment=comment
            )

            forum.comment_count += 1
            forum.save()
            notify.comment_notify(receiver=forum.author, status='comment', post=forum)
            return redirect('forum_detail', forum.id)

    context = {
        'post': forum,
        'comments': forum_comment,
        'other_post': other_forum,
        'date': checkDate(),
        'my_notification': notify.myNotifiction()
    }
    return render(request, 'forum/forum-detail.html', context)


def forum_post(request):
    other_forum = Forum.objects.all()[:5]
    notify = UserNotification(request.user)

    if request.method == 'POST':
        form = ForumForm(request.POST)

        if form.is_valid():
            forum = form.save(commit=False)
            forum.author = request.user
            forum.save()

            notify.post_notify(status='post', post=forum)
            return redirect('forum')
        else:
            mg.error(request, 'Not Successful!')



    context = {
        'forum': other_forum,
        'my_notification': notify.myNotifiction()
    }
    return render(request, 'forum/forum-form.html', context)



@login_required(login_url='login')
def repost(request, pk):
    forum = get_object_or_404(Forum, id=pk)
    notify = UserNotification(request.user)
    
    referer = request.META.get('HTTP_REFERER')
    pages.append(referer)

    Forum.objects.create(
        author=forum.author,
        title=forum.title,
        description=forum.description,
        owner=request.user
    )
    forum.repost.add(request.user)
    notify.repost_notify(status='repost', receiver=forum.author, post=forum)

    return redirect(f'{pages[-1]}')




def read_notify(request, pk):
    notify = get_object_or_404(Notification, id=pk)

    if notify.status == 'follow':
        notify.isRead = True
        notify.save()
        return redirect('dashboard', notify.sender.profile.id)
    else:
        notify.isRead = True
        notify.save()
        return redirect('forum_detail', notify.post.id)
    


def clear_all(request):
    notify = Notification.objects.all().filter(user=request.user, isRead=False)
    referer = request.META.get('HTTP_REFERER')
    pages.append(referer)

    for note in notify:
        note.isRead = True
        note.save()
    return redirect(f'{pages[-1]}')




def delete_post(request, pk):
    referer = request.META.get('HTTP_REFERER')
    # pages.clear()
    pages.append(referer)
    print(pages)
    post = get_object_or_404(Forum, id=pk)
    post.delete()
    mg.error(request, 'Post Deleted Successfully!!!')
    return redirect(f'{pages[-2]}')



@login_required(login_url='login')
def post_like(request, pk):
    post = get_object_or_404(Forum, id=pk)
    referer = request.META.get('HTTP_REFERER')
    notify = UserNotification(request.user)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return redirect(referer)
    else:
        post.likes.add(request.user)
        notify.like_notify(status='like', post=post, receiver=post.author)
        return redirect(referer)
    


@login_required(login_url='login')
def save_post(request, pk):
    post = get_object_or_404(Forum, id=pk)
    referer = request.META.get('HTTP_REFERER')

    try:
        save = get_object_or_404(SaveItem, item=post)
        if save:
            post.saved.remove(request.user)
            save.delete()
            return redirect(referer)
        

    except SaveItem.DoesNotExist:
        with transaction.atomic():
            SaveItem.objects.create(
                user = request.user,
                item = post
            )
            post.saved.add(request.user)
            mg.success(request, 'Post Saved!')
            return redirect(referer)


@login_required(login_url='login') 
def post_detail_like(request, pk):
    post = get_object_or_404(Forum, id=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return redirect('forum_detail', post.id)
    else:
        post.likes.add(request.user)
        return redirect('forum_detail', post.id)


@login_required(login_url='login')
def comment_like(request, pk, pd):
    comment = get_object_or_404(Comment, id=pk)
    post = get_object_or_404(Forum, id=pd)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        return redirect('forum_detail', post.id)
    else:
        comment.likes.add(request.user)
        return redirect('forum_detail', post.id)



@login_required(login_url='login')
def events_post(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        files = request.FILES.getlist("image")

        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()

            for i in files:
                Images.objects.create(blog=blog, image=i)  
            return redirect('blog')
        
    return render(request, 'forum/event.html')