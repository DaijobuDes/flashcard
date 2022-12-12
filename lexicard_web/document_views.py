import pathlib
from django.db import transaction
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View

from django.core.files.storage import FileSystemStorage
from datetime import date, timedelta, datetime
from django.utils.timezone import get_current_timezone

from .forms import *
from .generate import Generate


class DocumentView(View):
    """
    Class handler for the Document main page.

    Allowed methods:
    GET

    """
    template_name = "documents.html"

    def get(self, request):
        documents = Document.objects.filter(user_id = request.user)
        return render(request, self.template_name, {'documents':documents})
    
    """ Delete Document """
    def post(self, request, *args, **kwargs):        
        doc_ids = request.POST.getlist('id[]')
        for doc_id in doc_ids:
            print(doc_id)
            try:
                document = Document.objects.get(document_id=doc_id)  
                document.delete()
            except Document.DoesNotExist:
                document = None
        return redirect("viewAllDocs")  

class UploadDocumentView(View):
    """
    Class handler for the Upload Document page.

    Allowed methods:
    GET
    POST
    """
    template_name = "document-upload.html"

    def post(self, request):
        print("hahahha")
        form = UploadDocForm(request.POST, request.FILES)

        doc_files = request.FILES.getlist('doc_file')
        doc_list = [] #list of file url
        for doc_file in doc_files:
            doc_file = doc_file
            doc_format = pathlib.Path(doc_file.name).suffix.upper() #Get the file format from the file name and change it to uppercase. Example output: .PDF
            doc_format = doc_format.replace('.', "") #Remove the dot(.) in the front. Example Output: PDF
            date_mod = str(datetime.now(tz=get_current_timezone())+timedelta(hours=8))
           
            """ TODO: Check if valid file format """
            """ TODO: Check if unique name in regards with the user_id"""

            document = Document.objects.create(user_id = request.user, document_file = doc_file, document_name = doc_file.name, document_format = doc_format, date_modified = date_mod)     
            document.save()
            doc_list.append(document.document_name)
        return redirect("viewAllDocs")
    
    def get(self, request): 
        form = UploadDocForm()
        return render(request, self.template_name, {'form': form})

class RenameDocumentView(View):

    def post(self, request):
        id=request.POST.get('id','')
        type=request.POST.get('type','')
        value=request.POST.get('value','')
        #document = Document.objects.get(document_id=id) 
        print(value)

        if type=="name":
            name = value

        Document.objects.filter(document_id=id).update(document_name= name)
        
        return redirect("viewAllDocs")
    

