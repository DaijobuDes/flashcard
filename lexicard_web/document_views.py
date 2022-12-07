import pathlib
from django.db import transaction
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View

from django.core.files.storage import FileSystemStorage

from .forms import *
from .generate import Generate


class DocumentView(View):
    """
    Class handler for the main page.

    Allowed methods:
    GET

    """

    template_name = "documents.html"

    def get(self, request):
        return render(request, self.template_name)
def viewAllDocuments(request):
    documents = Document.objects.all()
    return render(request,"documents.html", {'documents':documents})

def uploadDocument(request):
    
    if request.method == 'POST':
        form = UploadDocForm(request.POST, request.FILES)

        """ if multiple files """
        doc_files = request.FILES.getlist('doc_file')
        doc_list = [] #list of file url
        for doc_file in doc_files:
            doc_file = doc_file
            doc_format = pathlib.Path(doc_file.name).suffix.upper() #Get the file format from the file name and change it to uppercase. Example output: .PDF
            doc_format = doc_format.replace('.', "") #Remove the dot(.) in the front. Example Output: PDF
         
            """ TODO: Check if valid file format """
            """ TODO: Check if unique name in regards with the user_id"""

            document = Document.objects.create(user_id = request.user, document_file = doc_file, document_name = doc_file.name, document_format = doc_format)     
            document.save()
            doc_list.append(document.document_file.url)

        """ single file upload """
        #doc_file = request.FILES['doc_file']
        #doc_format = pathlib.Path(doc_file.name).suffix.upper() #Get the file format from the file name and change it to uppercase. Example output: .PDF
        #doc_format = doc_format.replace('.', "") #Remove the dot(.) in the front. Example Output: PDF

        """ TODO: Check if valid file format """
        """ TODO: Check if unique name in regards with the user_id"""

        #document = Document.objects.create(user_id = request.user, document_file = doc_file, document_name = doc_file.name, document_format = doc_format)
        #document.save()
        return render(request, 'document-upload.html', {'url': doc_list})

    else:
        form = UploadDocForm()
    return render(request, 'document-upload.html', {'form': form})

def renameDocument(request, id):
    document = Document.objects.get(document_id=id) 
    form = DocumentForm(request.POST, instance=document) 
    if form.is_valid():
        document.save()  
        return redirect("viewAllDocs")
    else:
        return render(request, 'document.html', {'document':document})

def deleteDocument(request, id):
    document = Document.objects.get(document_id=id)  
    document.delete()  
    return redirect("viewAllDocs")      
    

