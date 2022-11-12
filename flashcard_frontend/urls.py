"""flashcard_frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from lexicard_web import flashcard_views, other_views, user_views

urlpatterns = [
    path(r'', lambda r: HttpResponseRedirect('/login')),
    path('admin/', admin.site.urls),
    path('login/', user_views.Login.as_view()),
    path('register/', user_views.Register.as_view()),
    path('logout/', user_views.Logout.as_view()),

    # Place /profile here
    path('profile/update/upload', user_views.UploadProfileView.as_view()),
    path('profile/', user_views.ProfileView.as_view()),

    # Flashcard urls
    path('flashcard/', flashcard_views.FlashcardView.as_view()),
    path('flashcard/create/', flashcard_views.FlashcardCreateView.as_view()),
    path('flashcard/generate/', flashcard_views.GenerateFlashcard.as_view()),
    #path('flashcard/flashcard/', views.FlashcardIndi.as_view()),

    # Schedule url here
    path('schedule/', other_views.ScheduleView.as_view()),\

    path('home/', other_views.DashboardView.as_view()),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
