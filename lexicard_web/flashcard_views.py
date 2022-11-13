from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View
from django.db import transaction
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

class FlashcardCreateView(View):
    template_name = "test.html"

    def get(self, request):
        return render(request, self.template_name)


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

        deck = Deck(
            user_id = request.user,
            document_id = document,
            deck_name = deck_name,
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