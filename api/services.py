import os
from datetime import datetime

from api.forms import ImageForm
from api.models import Likes, Photo, Subscriptions, User
from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.shortcuts import get_object_or_404


def create_user(request: HttpRequest, user: User) -> None:
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')
    user.bio = request.POST.get('bio')
    user.link = request.POST.get('link')
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    if user.link == '':
        user.link = user.username
    user.set_password(request.POST.get('password'))
    user.save()

def login_user(request: HttpRequest) -> User:
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    return user

def image_upload(request: HttpRequest) -> ImageForm:
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save(commit=False)
        image.time_creation = datetime.now()
        image.save()
    else:
        form = ImageForm()
    return form

def delete_photo(request: HttpRequest, photo: Photo) -> str:
    if request.user.id != photo.user_id:
        return 401
    else:
        photo.delete()
        photoImage = str(photo.image)
        os.remove(f'media/{photoImage}')
        return 200

def like_photo(request: HttpRequest, photo: Photo) -> None:
    like = Likes(photo_id=photo.id, user_id=request.user.id)
    like.save()
    photo.like_count +=1
    photo.save()

def dislike_photo(request, photo: Photo, like: Likes) -> None:
    like.delete()
    photo.like_count -=1
    photo.save()

def sub_on_user(request, user: User) -> None:
    new_sub = Subscriptions(following_user_id=request.user, user_id = user)
    user.sub_count +=1
    user.save()
    new_sub.save()

def unsub_on_user(user: User, sub_user: Subscriptions) -> None:
    sub_user.delete()
    user.sub_count -=1
    user.save()

def news_feed(sub: Subscriptions) -> list:
    content_maker = get_object_or_404(Subscriptions,following_user_id=sub.id)
    photo_list = Photo.objects.filter(user_id=content_maker.user_id).all()
    return(photo_list)
