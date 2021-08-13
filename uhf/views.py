from ganj.views import profileView
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from ganj.models import Follow, Post, Stream

from uhf.forms import ChangePasswordForm, EditProfileForm, SignupForm
from uhf.models import Profile


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            new_user = User.objects.create_user(username=username, email=email, password=password)
            authenticate(username=username, password=password)
            login(request, new_user)
            return redirect('index')
    else:
        form = SignupForm()
    context = {'form': form, }
    return render(request, 'signup.html', context)


@login_required
def PasswordChange(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_done')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'change_password.html', context)


def PasswordChangeDone(request):
    return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
    user = request.user
    profile = Profile.objects.get(user__id=user.id)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            in_first_name = form.cleaned_data.get('first_name')
            in_last_name = form.cleaned_data.get('last_name')
            in_info = form.cleaned_data.get('profile_info')
            in_pfp = form.cleaned_data.get('pfp')
            # in_pfp = request.FILES['pfp'] ------ BOTH WORK
            if in_first_name:
                profile.user.first_name = in_first_name
                profile.user.save()
            if in_last_name:
                profile.user.last_name = in_last_name
                profile.user.save()
            if in_info:
                profile.profile_info = in_info
            if in_pfp:
                profile.pfp = in_pfp
            profile.save()
            return redirect('profile')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
    }
    return render(request, 'edit_profile.html', context)


@login_required
def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)
    try:
        f, created = Follow.objects.get_or_create(
            follower=user, following=following)
        if int(option) == 0:  # we are unfollowing
            following.profile.xp -= 1
            following.profile.save()
            f.delete()
            Stream.objects.filter(following=following,
                                  user=user).all().delete()
        else:  # we are following
            following.profile.xp += 1
            following.profile.save()
            posts = Post.objects.all().filter(user=following)[
                :15]  # following's last 15 posts
            with transaction.atomic():  # add new posts streams
                for post in posts:
                    stream = Stream(post=post, user=user,
                                    date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('others_profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('others_profile', args=[username]))
