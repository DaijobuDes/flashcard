import random
import time
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseServerError, JsonResponse)
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View
from django.db import transaction
from django.db.models import Avg, Min, Max
from .forms import *
from .generate import Generate
from django.contrib import messages
from PIL import Image
import io
import zipfile


class FlashcardView(View):
    """
    Class handler for the available flashcard page.

    Allowed methods:
    GET POST

    """
    template_name = "flashcards.html"

    def get(self, request):
        flashcard = Flashcard.objects.filter(
            user_id = request.user.user_id
        )

        context = {
            "flashcard": flashcard,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        notif = request.POST.get('notifs')
        User.objects.filter(user_id=request.user.user_id).update(notifs = True if notif == "True" else False)
        return redirect('/flashcard/')


class FlashcardRenameView(View):
    """
    Class handler for the available flashcard page.

    Allowed methods:
    GET POST

    """
    template_name = "flashcards-edit.html"

    def get(self, request):
        flashcard = Flashcard.objects.filter(
            user_id = request.user.user_id
        )

        context = {
            "flashcard": flashcard,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        return render(request, self.template_name)


class FlashcardDeleteView(View):
    """
    Class handler for the available flashcard page.

    Allowed methods:
    GET POST

    """
    template_name = "flashcard-delete.html"

    def get(self, request):
        flashcard = Flashcard.objects.filter(
            user_id = request.user.user_id
        )

        context = {
            "flashcard": flashcard,
        }

        return render(request, self.template_name, context)

class FlashcardDelete(View):
    def get(self, request, deck_id):
        if not Deck.objects.filter(deck_id = deck_id).exists():
            return redirect('/flashcard/')

        Deck.objects.filter(deck_id = deck_id).delete()
        return redirect("/flashcard/")

class DeckView(View):
    template_name = "flashcard.html"

    def get(self, request, deck_id):
        if not Deck.objects.filter(deck_id = deck_id).exists():
            return redirect('/home/')

        flash = Flashcard.objects.get(
            deck_id = deck_id
        )

        qa = QA.objects.filter(
            flashcard_id = flash.flashcard_id
        )

        deck = Deck.objects.get(deck_id = deck_id)

        context = {
            'qa' : qa,
            'len' : qa.count(),
            'deck' : deck
        }

        return render(request, self.template_name, context)

    def post(self, request, deck_id):
        """
        TODO: Do deletion stuff here
        """
        pass

class EditDeckView(View):
    template_name = "flashcard-rename.html"
    """
    TODO: name checking if exists
    """

    def get(self, request, deck_id):
        if not Deck.objects.filter(deck_id = deck_id).exists():
            return redirect('/home/')

        deck = Deck.objects.get(deck_id = deck_id)

        context = {
            'deck' : deck
        }

        return render(request, self.template_name, context)

    def post(self, request, deck_id):

        if not Deck.objects.filter(deck_id = deck_id).exists():
            return redirect('/home/')

        rename = request.POST.get("rename")
        # deck_id = request.POST.get("deck_id")

        Deck.objects.filter(deck_id=deck_id).update(deck_name=rename)

        Deck.objects.get(deck_id=deck_id)

        return redirect("/flashcard")

class EditDeckItem(View):

    template_name = "edit-question.html"

    def get(self, request, deck_id, qa_id):
        flashcard = Flashcard.objects.get(deck_id=deck_id)

        qa = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id,
            QA_id=qa_id
        ).first()

        context = {
            "qa": qa
        }

        return render(request, self.template_name, context)

    def post(self, request, deck_id, qa_id):
        question = request.POST.get("question")
        answer = request.POST.get("answer")

        flashcard = Flashcard.objects.get(deck_id=deck_id)

        qa = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id,
            QA_id=qa_id
        ).update(
            flashcard_question=question,
            flashcard_answer=answer
        )

        return redirect(f"/flashcard/view/{deck_id}")



class FlashcardCreateView(View):
    template_name = "test.html"

    def get(self, request):
        prefs = User.objects.get(user_id=request.user.user_id)
        classes = Classes.objects.filter(user_id=request.user)
        context = {
            "prof" : prefs,
            "classes" : classes,
        }
        return render(request, self.template_name, context)


    def post(self, request):

        file = request.FILES['file']
        file_extension = file.name.split(".")[-1].upper()

        valid_file_types = [
            "PPT", "PPTX", "DOC", "DOCX", "RTF", "TXT", "PDF"
        ]

        if file_extension not in valid_file_types:
            # return redirect("/")
            return JsonResponse({
                "message": "Invalid file type.",
                "hint": "Upload a valid file type.",
                "upload": file_extension,
                "formats": [
                    "PPT", "PPTX", "DOC", "DOCX", "RTF", "TXT", "PDF"
                ]
            })

        questions_array = []
        answers_array = []

        questions_array = request.POST.getlist("question")
        answers_array = request.POST.getlist("answer")

        print(questions_array)
        print(answers_array)

        # questions_array.append(request.POST.getlist("question"))
        # answers_array.append(request.POST.getlist("answer"))

        deck_name = request.POST.get("deckName")
        class_id = request.POST['classes']

        document = Document(
            user_id = request.user,
            document_name = file.name,
            document_file = file,
            document_format = file_extension,
        )

        document.save()

        cl = Classes.objects.get(classes_id=class_id)

        deck = Deck(
            user_id = request.user,
            document_id = document,
            deck_name = deck_name,
            classes_id = cl,
        )

        deck.save()

        flash = Flashcard(
            user_id = request.user,
            deck_id = deck,
        )

        flash.save()

        with transaction.atomic():
            for x, y in zip(questions_array, answers_array):
                data = QA.objects.create(
                    flashcard_question = x,
                    flashcard_answer = y,
                    flashcard_id = flash,
                )
                data.save()

        return redirect("/flashcard/view/" + str(deck.deck_id))

class FlashcardDownload(View):
    template_name = "flashcards-download.html"

    def get(self, request):

        deck = Deck.objects.filter(user_id=request.user.user_id)
        context = {
            "deck" : deck,
        }
        return render(request, self.template_name, context)

class GenerateFlashcard(View):
    """
    Comments here
    """

    template_name = "generate.html"

    def get(self, request, deck_id):
        # Pass the list of terms and answers
        # Reference: https://stackoverflow.com/questions/6977544/rar-zip-files-mime-type
        #
        # Possible file MIME types
        # application/zip, application/octet-stream, application/x-zip-compressed, multipart/x-zip
        data = Generate()

        flash = Flashcard.objects.get(
            deck_id = deck_id,
            user_id = request.user.user_id
        )

        qa = QA.objects.filter(
            flashcard_id = flash.flashcard_id
        )

        questions = [x.flashcard_question for x in qa]
        answers = [x.flashcard_answer for x in qa]

        # return JsonResponse(
        #     {
        #         "questions": questions,
        #         "answers": answers
        #     }
        # )

        generation = data.save_zip(request.user.user_id, deck_id, questions, answers)

        # Terminate if variable is not a valid zipfile
        assert zipfile.is_zipfile(generation)

        data = HttpResponse(generation.getbuffer(), content_type="application/zip")
        data['Content-Disposition'] = f'attachment; filename="flashcard_deck{deck_id}.zip"'

        return data

class FlashcardRandomQuestionAndAnswer(View):
    # NOTE: Code optimization is needed
    # NOTE: What works here
    #       1. Question randomization works
    #       2. Answers also works
    #       3. Probably a bit of moodle style? Answers are word sensitive
    template_name = "random-question-and-answer.html"

    def get(self, request, deck_id):
        flashcard = Flashcard.objects.get(deck_id=deck_id)

        qa = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id
        )

        random.seed(time.time())

        random_question = random.choice(list(qa))

        print(random_question)

        context = {
            "qa": random_question,
            "flashcard": flashcard
        }

        return render(request, self.template_name, context)

    def post(self, request, deck_id):

        question_id = request.POST.get("id")
        answer = request.POST.get("answer")

        flashcard = Flashcard.objects.get(deck_id=deck_id)

        qa = QA.objects.get(
            QA_id=question_id,
            flashcard_id_id=flashcard.flashcard_id
        )

        qas = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id
        )

        random.seed(time.time())

        random_question = random.choice(list(qas))

        context = {
            "qa": random_question
        }

        if qa.flashcard_question.lower() == answer.lower():
            messages.error(request, 'Correct Answer')
            return render(request, self.template_name, context)

        messages.error(request, 'Wrong Answer')
        return render(request, self.template_name, context)

            # return JsonResponse(
            #     {
            #         "status": "200",
            #         "message": "Correct answer"
            #     }
            # )

        # return JsonResponse(
        #     {
        #         "status": "200",
        #         "message": "Wrong answer"
        #     }
        # )

class FlashcardQuestionAndAnswer(View):
    # NOTE: Code optimization is needed
    # NOTE: What works here
    #       1. Question randomization works
    #       2. Answers also works
    #       3. Probably a bit of moodle style? Answers are word sensitive
    template_name = "question-and-answer.html"

    def get(self, request, deck_id, question_id, action):
        flashcard = Flashcard.objects.get(deck_id=deck_id)

        check = True
        qa = None
        max_id = 1
        # Get max ID number
        max_id = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id,
        ).aggregate(Max("QA_id")).get("QA_id__max", 1)

        # TODO: Fix infinite loop
        # NOTE: Probably fixed, 11/22/22 02:53
        print(action)
        while check is True:
            qa = QA.objects.filter(
                flashcard_id_id=flashcard.flashcard_id,
                QA_id=question_id
            )

            if qa.exists():
                check = False

            if action == "next":
                if question_id <= max_id:
                    question_id += 1
                else:
                    question_id = max_id
            if action == "prev":
                if question_id <= 1:
                    question_id = 1
                else:
                    question_id -= 1

        context = {
            "qa": qa.first(),
            "question_id": question_id
        }

        return render(request, self.template_name, context)

    def post(self, request, deck_id, question_id, action):
        question_id = request.POST.get("id")
        answer = request.POST.get("answer")

        flashcard = Flashcard.objects.get(deck_id=deck_id)

        qa = QA.objects.get(
            QA_id=question_id,
            flashcard_id_id=flashcard.flashcard_id
        )

        if qa.flashcard_answer.lower() == answer.lower():
            return JsonResponse(
                {
                    "status": "200",
                    "message": "Correct answer"
                }
            )

        return JsonResponse(
            {
                "status": "200",
                "message": "Wrong answer"
            }
        )

class FlashcardRemoveQuestion(View):

    template_name = "delete-question.html"

    def get(self, request, deck_id):
        flashcard = Flashcard.objects.get(deck_id=deck_id)

        qa = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id,
        )

        context = {
            "qa": qa
        }

        return render(request, self.template_name, context)

    def post(self, request, deck_id):
        question_id = request.POST.get("id")

        flashcard = Flashcard.objects.get(deck_id=deck_id)

        qa = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id,
            QA_id=question_id
        ).delete()

        return redirect(f"/flashcard/view/{deck_id}/delete")

class EditPrefView(View):
    def post(self, request):
        profile = User.objects.filter(user_id=request.user.user_id);

        term_bg = request.POST.get("term_bg")
        term_txt = request.POST.get("term_txt")
        question_bg = request.POST.get("question_bg")
        question_txt = request.POST.get("question_txt")

        profile.update(
            term_bg_color = term_bg,
            term_txt_color = term_txt,
            question_bg_color = question_bg,
            question_txt_color = question_txt,
        )
        return redirect("viewAllDocs")