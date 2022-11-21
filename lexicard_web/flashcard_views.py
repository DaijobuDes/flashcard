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
        return render(request, self.template_name)

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
        return render(request, self.template_name, {"classes": Classes.objects.filter(user_id=request.user)})


    def post(self, request):
        questions_array = []
        answers_array = []

        questions_array = request.POST.getlist("question")
        answers_array = request.POST.getlist("answer")

        # questions_array.append(request.POST.getlist("question"))
        # answers_array.append(request.POST.getlist("answer"))

        deck_name = request.POST.get("deckName")
        # print(questions_array)

        print(questions_array[0])


        # This portion STILL NEEDS WORK!
        document = Document(
            user_id = request.user,
            document_name = questions_array[0],
            document_format = "DOC",
        )
        document.save()

        class_ = Classes.objects.get(user_id_id=request.user)

        deck = Deck(
            user_id = request.user,
            document_id = document,
            deck_name = deck_name,
            classes_id = class_,
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
                print(x)
                data.save()

        return redirect("/flashcard/view/" + str(deck.deck_id))

class GenerateFlashcard(View):
    """
    Class handler for generating flashcards.

    Allowed methods:
    GET POST

    """

    template_name = "generate.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        term = request.POST.get("term")
        definition = request.POST.get("definition")

        data = Generate()
        data.setTerm(term)
        data.setDefinition(definition)
        response = HttpResponse(content_type='image/png')
        image = data.saveImage(response)
        return HttpResponse(response, content_type='image/png')

        # return HttpResponse(json.dumps(
        #     {
        #         "term": term,
        #         "definition": definition,
        #     }
        # ))

        return render(request, self.template_name, {"image": image})

class FlashcardRandomQuestionAndAnswer(View):
    # NOTE: Code optimization is needed
    # NOTE: What works here
    #       1. Question randomization works
    #       2. Answers also works
    #       3. Probably a bit of moodle style? Answers are word sensitive
    template_name = "question-and-answer.html"

    def get(self, request, deck_id):
        flashcard = Flashcard.objects.get(deck_id=deck_id)

        qa = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id
        )

        random.seed(time.time())

        random_question = random.choice(list(qa))

        print(random_question)

        context = {
            "qa": random_question
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
        # max_id = QA.objects.filter(
        #     flashcard_id_id=flashcard.flashcard_id,
        # ).aggregate(Max("QA_id"))

        # TODO: Fix infinite loop
        # NOTE: Probably fixed, 11/22/22 02:53
        while check is True:
            qa = QA.objects.filter(
                flashcard_id_id=flashcard.flashcard_id,
                QA_id=question_id
            )

            if qa.exists():
                check = False
                break

            if action == "next":
                if question_id <= max_id:
                    question_id += 1
                else:
                    question_id = max_id
            elif action == "prev":
                if question_id >= 1:
                    question_id = 1
                else:
                    question_id -= 1


        context = {
            "qa": qa
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