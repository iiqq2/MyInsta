from api.models import Likes, Photo, Subscriptions, User
from api.services import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View


class IndexUser(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        users = User.objects.all()
        return render(request, 'index.html', {'users': users})


class CreateUser(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user = User()
        create_user(request, user)
        return redirect(f'/user/{user.link}')


class UserInf(View):
    def get(self, request: HttpRequest, user_link: str) -> HttpResponse | HttpResponseNotFound:
        try:
            user = User.objects.get(link=user_link)
            images = Photo.objects.filter(user_id=user.id).all()
            return render(request, 'info_user.html', {'user': user, 'photos': images})
        except User.DoesNotExist:
            return HttpResponseNotFound('<h2>User not found</h2>')


class LoginUser(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user = login_user(request)
        if user is not None:
            login(request, user)
            return redirect(f'/user/{user.link}')
        else:
            return HttpResponse('<h1>fail try to login</h1>')


class Log(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        users = User.objects.all()
        return render(request, 'login.html', {'users': users})


def logout_user(request: HttpRequest, user_link) -> HttpResponse:
    logout(request)
    return redirect('http://127.0.0.1:8000')  # Изменить при загрузке на сервер


class ImageUpload(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = ImageForm()
        return render(request, 'add_photo.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = image_upload(request)
        return render(request, 'add_photo.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class DeletePhoto(View):
    def post(self, request: HttpRequest, user_link: str, photo_id: int) -> HttpResponse:
        user = get_object_or_404(User, link=user_link)
        photo = get_object_or_404(Photo, id=photo_id, user_id=user.id)
        status = delete_photo(request, photo)
        if status == 401:
            return redirect('/login_user')
        else:
            return redirect('user_inf', user_link=user_link)


@method_decorator(login_required, name='dispatch')
class LikePhoto(View):
    def post(self, request: HttpRequest, user_link: str, photo_id: int) -> HttpResponse:
        photo = get_object_or_404(Photo, id=photo_id)
        try:
            like = Likes.objects.get(photo_id=photo.id, user_id=request.user.id)
        except Likes.DoesNotExist:
            like_photo(request, photo)
            return redirect('user_inf', user_link=user_link)
        else:
            dislike_photo(request, photo, like)
            return redirect('user_inf', user_link=user_link)


@method_decorator(login_required, name='dispatch')
class NewsFeed(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        sub = get_object_or_404(User, id=request.user.id)
        images = news_feed(sub)
        return render(request, 'news_feed.html', {'photos': images})


@method_decorator(login_required, name='dispatch')
class SubUser(View):
    def post(self, request: HttpRequest, user_link: str) -> HttpResponse:
        user = get_object_or_404(User, link=user_link)
        if request.user.id != user.id:
            try:
                sub_user = Subscriptions.objects.get(following_user_id=request.user, user_id=user)
            except Subscriptions.DoesNotExist:
                sub_on_user(request, user)
                return redirect('user_inf', user_link=user_link)
            else:
                unsub_on_user(user, sub_user)
                return redirect('user_inf', user_link=user_link)
        else:
            return HttpResponse(r'<h1>Невозможно подписаться на самого себя, лучше найди друзей и тогда они смогут на тебя подписываться :( сори что давлю, но чувак реально найди друзей и все будет круто\</h1>')


class HomePage(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'home.html')
