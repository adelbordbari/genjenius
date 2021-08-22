from comments.forms import CommentForm, NoteForm
from comments.models import Comment, Note
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.db.models import Q, Count
from django.views.generic import RedirectView
from slugify import slugify_unicode

from .forms import EditPostForm, NewPostForm
from .models import Follow, Post, Stream, Tag

#########################################DONE###########################################


def homeView(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render({}, request))

def contactView(request):
    template = loader.get_template('contact.html')
    return HttpResponse(template.render({}, request))


def fourohfourView(request):
    template = loader.get_template('404.html')
    return HttpResponse(template.render({}, request))


@login_required
def userFollowingsView(request, username):
    user = get_object_or_404(User, username=username)
    return followingsView(request, user)


@login_required
def followingsView(request, dst=None):
    if dst == None:
        dst_user = request.user
    else:
        dst_user = dst
    followings = Follow.objects.filter(follower=dst_user)
    followings_list = []
    for f in followings:
        followings_list.append(f.following)
    prev = 'followings'
    paginator = Paginator(followings_list, 5)
    page_number = request.GET.get('page')
    try:
        # returns the desired page object
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)

    template = loader.get_template('index.html')
    context = {
        'page_obj': page_obj,
        'dst_user': dst_user,
        'prev': prev,
    }
    return HttpResponse(template.render(context, request))


@login_required
def editPostView(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user.username == request.user.username:
        tags_objs = []
        if request.method == 'POST':
            form = EditPostForm(request.POST)
            if form.is_valid():
                in_title = form.cleaned_data.get('title')
                in_author = form.cleaned_data.get('author')
                in_tags = form.cleaned_data.get('tags')
                tags_list = list(in_tags.split(' '))
                for tag in tags_list:
                    t, created = Tag.objects.get_or_create(
                        slug=slugify_unicode(tag), title=tag)
                    tags_objs.append(t)
                if in_title:
                    post.title = in_title
                if in_author:
                    post.author = in_author
                if in_tags:
                    post.tags.set(tags_objs)
                post.save()
                return redirect('index')
        else:
            form = EditPostForm()
        context = {'form': form, }
        return render(request, 'edit_post.html', context)
    return HttpResponseRedirect(reverse('404'))


@login_required
def deletePostView(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user.username == request.user.username:
        if request.method == 'POST':
            post.delete()
        else:
            return render(request, 'delete_post.html', {'post': post})
    return HttpResponseRedirect(reverse('404'))


@login_required
def userFollowersView(request, username):
    user = get_object_or_404(User, username=username)
    return followersView(request, user)


@login_required
def followersView(request, dst=None):
    if dst == None:
        dst_user = request.user
    else:
        dst_user = dst
    followers = Follow.objects.filter(following=dst_user)
    followers_list = []
    for f in followers:
        followers_list.append(f.follower)
    prev = 'followers'
    paginator = Paginator(followers_list, 5)
    page_number = request.GET.get('page')
    try:
        # returns the desired page object
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)

    template = loader.get_template('index.html')
    context = {
        'page_obj': page_obj,
        'dst_user': dst_user,
        'prev': prev,
    }
    return HttpResponse(template.render(context, request))


@login_required
def searchView(request):
    query = request.GET.get('search_box')
    if query.startswith('@'):  # user search
        prev = 'u_search'
        query = query[1:]
        user_items = User.objects.filter(Q(username__icontains=query) | Q(
            first_name__icontains=query) | Q(last_name__icontains=query)).order_by("-date_joined")
        paginator = Paginator(user_items, 10)
    else:
        prev = 'q_search'
        post_items = Post.objects.filter(Q(body__icontains=query) | Q(
            title__icontains=query)).order_by('-posted')
        paginator = Paginator(post_items, 5)

    page_number = request.GET.get('page')
    try:
        # returns the desired page object
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)
    template = loader.get_template('index.html')

    context = {
        'page_obj': page_obj,
        'q': query,
        'prev': prev,
    }
    return HttpResponse(template.render(context, request))


@login_required
def authorView(request, author):
    author_posts = Post.objects.filter(author=author).order_by("-posted")
    prev = 'author_search'
    paginator = Paginator(author_posts, 5)
    page_number = request.GET.get('page')
    try:
        # returns the desired page object
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)
    template = loader.get_template('index.html')
    context = {
        'author': author,
        'page_obj': page_obj,
        'prev': prev
    }
    return HttpResponse(template.render(context, request))


@login_required
def tagsView(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    post_items = Post.objects.filter(tags=tag).order_by('-posted')
    paginator = Paginator(post_items, 5)
    page_number = request.GET.get('page')
    try:
        # returns the desired page object
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)
    prev = 'tag_search'
    template = loader.get_template('index.html')
    context = {'post_items': post_items, 'page_obj': page_obj, 'tag': tag, 'prev': prev}
    return HttpResponse(template.render(context, request))


def aboutView(request):
    return render(request, 'about.html', {})


def cocView(request):
    return render(request, 'coc.html', {})


def guidelinesView(request):
    return render(request, 'guidelines.html', {})


@login_required
def indexView(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(
        id__in=group_ids) | Post.objects.filter(user=user)
    post_items = post_items.order_by('-posted')

    paginator = Paginator(post_items, 5)
    page_number = request.GET.get('page')
    try:
        # returns the desired page object
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)

    template = loader.get_template('index.html')
    context = {
        'post_items': post_items,
        'page_obj': page_obj,
    }
    return HttpResponse(template.render(context, request))


@login_required
def writeView(request):
    user = request.user
    tags_objs = []
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            user.profile.xp += 1
            user.profile.save()
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            tags_form = form.cleaned_data.get('tags')
            author = form.cleaned_data.get('author')
            tags_list = list(tags_form.split(' '))
            for tag in tags_list:
                t, created = Tag.objects.get_or_create(
                    slug=slugify_unicode(tag), title=tag)
                tags_objs.append(t)
        p, created = Post.objects.get_or_create(
            user_id=user.id, body=body, title=title, author=author)
        p.author = author
        p.tags.set(tags_objs)
        p.save()
        return redirect('index')
    else:
        form = NewPostForm()
    authors = [f.author for f in Post.objects.all()]
    context = {'form': form, 'authors': set(authors)}
    return render(request, 'newpost.html', context)


@login_required
def detailsView(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by("-date")
    notes = Note.objects.filter(post=post).order_by('-date')
    form1 = CommentForm()
    form2 = NoteForm()
    template = loader.get_template('post_details.html')
    context = {
            'post': post,
            'comments': comments,
            'notes': notes,
            'comment_form': form1,
            'note_form': form2, 
            }

    if request.method == "GET":
        return HttpResponse(template.render(context, request))

    elif request.method == "POST":
        if 'btnComment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = user
                comment.save()
                user.profile.xp += 1
                user.profile.save()
        elif 'btnNote' in request.POST:
            form = NoteForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                note = form.save(commit=False)
                note.portion = data['portion']
                note.body = data['body']
                note.post = post
                note.user = user
                note.save()
                user.profile.xp += 1
                user.profile.save()
    return HttpResponseRedirect(reverse('post_details', args=[post.id]))
   

class likeToggleView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        url_ = post.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                post.likes.remove(user)
                post.user.profile.xp -= 1
                post.user.profile.save()
            else:
                post.likes.add(user)
                post.user.profile.xp += 1
                post.user.profile.save()
        return url_

class pasandView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        note_uuid = self.kwargs.get("note_uuid")
        note = get_object_or_404(Note, id=note_uuid)
        url_ = note.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in note.likes.all():
                note.likes.remove(user)
                note.user.profile.xp -= 1
                note.user.profile.save()
            else:
                note.likes.add(user)
                note.user.profile.xp += 1
                note.user.profile.save()
        return url_
        

@login_required
def userProfileView(request, username):
    user = get_object_or_404(User, username=username)
    return profileView(request, user)


@login_required
def profileView(request, dst=None):
    if dst == None:
        dst_user = request.user
    else:
        dst_user = dst
    posts = Post.objects.filter(user=dst_user).order_by('-posted')
    posts_count = posts.count()
    profile = dst_user.profile
    following_count = Follow.objects.filter(follower=dst_user).count()
    follower_count = Follow.objects.filter(following=dst_user).count()
    follow_status = Follow.objects.filter(
        following=dst_user, follower=request.user).exists()
    xp = dst_user.profile.xp

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    try:
        # returns the desired page object
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)

    template = loader.get_template('profile.html')
    context = {
        'dst_user': dst_user,
        'profile': profile,
        'posts_count': posts_count,
        'following_count': following_count,
        'followers_count': follower_count,
        'follow_status': follow_status,
        'page_obj': page_obj,
        'xp': xp
    }
    return HttpResponse(template.render(context, request))

