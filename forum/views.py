from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Forum, Comment
from django.db import transaction
from django.core.paginator import Paginator
from user_auth.models import Profile
from .forms import *
from django.contrib import messages as mg

# Create your views here.

# Checking and keeping track of pages
pages = []


@login_required(login_url='login')
def dashboard(request, pk):
    user_profile = Profile.objects.get(id=pk)
    user_posts = Forum.objects.all().filter(author=user_profile.user)
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
        'total_likes': total_likes
    }
    return render(request, 'forum/author.html', context)


def edit_profile(request, pk):
    user_profile = Profile.objects.get(id=pk)
    user = request.user
    error_msg = ''

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        level = request.POST.get('level')
        username = request.POST.get('username')
        tiktok = request.POST.get('tiktok')
        print(level)

        tiktok = tiktok.strip()

        if tiktok.startswith('@'):
            tiktok = tiktok
        else: tiktok = f'@{tiktok}' 

        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            user.first_name = first_name
            user.last_name = last_name
            user.level = level
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
        'user_profile': user_profile
    }
    return render(request, 'forum/dashboard-setting.html', context)


def follow(request, pk):
    profile = Profile.objects.get(id=pk)

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        return redirect('dashboard', profile.id)
    else:
        profile.followers.add(request.user)
        return redirect('dashboard', profile.id)


@login_required(login_url='login')
def forum(request):
    forum = Forum.objects.all()

    paginator = Paginator(forum, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'forum': forum,
        'page_obj': page_obj
    }
    return render(request, 'forum/forum.html', context)



@login_required(login_url='login')
def edit_forum(request, pk):
    forum = Forum.objects.get(id=pk)
    form = ForumForm(instance=forum)
    edit = True
    referer = request.META.get('HTTP_REFERER')
    pages.append(referer)
    other_forum = [x for x in Forum.objects.all()[:5] if x != forum]

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
        'forum': other_forum 
    }
    return render(request, 'forum/forum-form.html', context)

@login_required(login_url='login')
def forum_detail(request, pk):
    forum = Forum.objects.get(id=pk)
    forum_comment = forum.comment_set.all()

    # TRACING THE VISTED PAGES 
    pages.append(request.META.get('HTTP_REFERER'))

    # Checking and increasing the number of views
    if request.user not in forum.views.all():
        forum.views.add(request.user)

    other_forum = [x for x in Forum.objects.all()[:5] if x != forum]

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
            return redirect('forum_detail', forum.id)

    context = {
        'post': forum,
        'comments': forum_comment,
        'other_post': other_forum
    }
    return render(request, 'forum/forum-detail.html', context)


def forum_post(request):
    other_forum = Forum.objects.all()[:5]

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Forum.objects.create(
            author=request.user,
            title=title,
            description=description
        )
        return redirect('forum')

    context = {
        'forum': other_forum
    }
    return render(request, 'forum/forum-form.html', context)


def delete_post(request, pk):
    referer = request.META.get('HTTP_REFERER')
    pages.append(referer)
    print(pages)
    post = Forum.objects.get(id=pk)
    post.delete()
    mg.error(request, 'Post Deleted Successfully!!!')
    return redirect(f'{pages[-2]}')



@login_required(login_url='login')
def post_like(request, pk):
    post = Forum.objects.get(id=pk)
    referer = request.META.get('HTTP_REFERER')

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return redirect(referer)
    else:
        post.likes.add(request.user)
        return redirect(referer)


@login_required(login_url='login') 
def post_detail_like(request, pk):
    post = Forum.objects.get(id=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return redirect('forum_detail', post.id)
    else:
        post.likes.add(request.user)
        return redirect('forum_detail', post.id)


@login_required(login_url='login')
def comment_like(request, pk, pd):
    comment = Comment.objects.get(id=pk)
    post = Forum.objects.get(id=pd)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        return redirect('forum_detail', post.id)
    else:
        comment.likes.add(request.user)
        return redirect('forum_detail', post.id)
