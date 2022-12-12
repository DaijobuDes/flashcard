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
from lexicard_web import flashcard_views, other_views, user_views, document_views, schedule_views

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
    path('flashcard/create/', flashcard_views.FlashcardCreateView.as_view(), name='deck_view'),
    path('flashcard/generate/', flashcard_views.FlashcardDownload.as_view()),
    path('flashcard/generate/<int:deck_id>', flashcard_views.GenerateFlashcard.as_view()),
    path('flashcard/view/<int:deck_id>', flashcard_views.DeckView.as_view(), name='deck_view'),
    path('flashcard/edit/', flashcard_views.FlashcardRenameView.as_view()),
    path('flashcard/edit/<int:deck_id>', flashcard_views.EditDeckView.as_view(), name='deck_view'),
    path('flashcard/delete/', flashcard_views.FlashcardDeleteView.as_view()),
    path('flashcard/delete/<int:deck_id>', flashcard_views.FlashcardDelete.as_view(), name='deck_view'),
    path('flashcard/view/<int:deck_id>/edit/<int:qa_id>', flashcard_views.EditDeckItem.as_view()),
    path('flashcard/view/<int:deck_id>/quiz', flashcard_views.FlashcardRandomQuestionAndAnswer.as_view()),
    path('flashcard/view/<int:deck_id>/quiz/<int:question_id>/<str:action>', flashcard_views.FlashcardQuestionAndAnswer.as_view()),
    path('flashcard/view/<int:deck_id>/delete', flashcard_views.FlashcardRemoveQuestion.as_view()),

    # Classes
    path('classes/', other_views.ClassesView.as_view()),
    path('classes/view/<int:classes_id>', other_views.ClassView.as_view()),
    path('classes/create/', other_views.ClassCreateView.as_view()),

    # Document urls
    path('document/', document_views.DocumentView.as_view(), name='viewAllDocs'),
    path('document/upload/',document_views.UploadDocumentView.as_view(), name='uploadDoc'),
    path('document/rename/',document_views.RenameDocumentView.as_view(), name='renameDoc'),


    # Schedule url here
    path('schedule/', schedule_views.ScheduleView.as_view(), name='viewAllSched'),
    path('schedule/create/', schedule_views.CreateSchedView.as_view(), name='createSched'),
    #path('schedule/delete/',schedule_views.DeleteSchedView.as_view(), name='deleteSched'),
    #path('schedule/update/',schedule_views.UpdateSchedView.as_view(), name='updateSched'),
    path('schedule/update/',schedule_views.UpdateSchedView.as_view(), name='updateSched'),



    path('home/', other_views.DashboardView.as_view()),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
