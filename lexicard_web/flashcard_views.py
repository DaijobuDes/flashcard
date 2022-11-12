from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View
from .forms import *
from .generate import Generate

class FlashcardView(TemplateView):
    """
    Class handler for the available flashcard page.

    Allowed methods:
    GET POST

    """
    template_name = "flashcards.html"

class FlashcardCreateView(View):
    template_name = "create-flashcard.html"

    def get(self, request):
        return render(request, self.template_name)


    def post(self, request):
        questions_array = []
        answers_array = []
        questions_array.append(request.POST.get("question"))
        answers_array.append(request.POST.get("answer"))

        flash = Flashcard(
            user_id = request.user.user_id,
            deck_id = request.user.user_id
        )

        flash.save()

        while i < len(questions_array):
            data = QA(
                flashcard_id = flash.flashcard_id,
                flashcard_question = questions_array[i],
                flashcard_answer = answers_array[i]
            )
            data.save()
            i = i + 1

        return redirect("/flashcard/")

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