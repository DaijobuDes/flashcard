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
        documents = Document.objects.filter(user_id = request.user).order_by('document_id')
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
        notif = request.POST.get('notifs')
        User.objects.filter(user_id=request.user.user_id).update(notifs = True if notif == "True" else False)
        return redirect("viewAllDocs")

class DownloadDocumentView(View):
    def get(self, request, document_id):
        docu = Document.objects.get(document_id=document_id)
        filename = docu.document_name
        directory = docu.document_file
        format = docu.document_format.upper()

        mime_type_file_formats = {
            "PPT": "application/vnd.ms-powerpoint",
            "PPTX": "application/vnd.ms-powerpoint",
            "DOC": "application/msword",
            "DOCX": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "RTF": "application/rtf",
            "TXT": "text/plain",
            "PDF": "application/pdf"
        }

        mime_type = None

        if format in mime_type_file_formats:
            mime_type = mime_type_file_formats.get(format, 0)

        if mime_type == 0:
            mime_type = "text/plain"

        data = HttpResponse(directory, content_type=mime_type)
        data['Content-Disposition'] = f'attachment; filename="{filename}"'
        print("test")
        return data

class UploadDocumentView(View):
    """
    Class handler for the Upload Document page.

    Allowed methods:
    GET
    POST
    """
    template_name = "document-upload.html"

    def post(self, request):
        form = UploadDocForm(request.POST, request.FILES)

        doc_files = request.FILES.getlist('doc_file')
        doc_list = [] #list of file url
        for doc_file in doc_files:
            doc_file = doc_file
            doc_name = pathlib.Path(doc_file.name).stem
            print(doc_name)
            doc_format = pathlib.Path(doc_file.name).suffix.upper() #Get the file format from the file name and change it to uppercase. Example output: .PDF
            doc_format = doc_format.replace('.', "") #Remove the dot(.) in the front. Example Output: PDF
            date_mod = str(datetime.now(tz=get_current_timezone())+timedelta(hours=8))

            """ TODO: Check if valid file format """
            flag = 1
            for k, f in Document.FILE_FORMAT:
                print(k)
                if(doc_format == k):  
                    flag = 1
                    break
                else:
                    flag = 0;    

            if(flag == 0):
                return render(request, self.template_name, {'invalidfileformat': 'Invalid file format!'})
            else:
                document = Document.objects.create(user_id = request.user, document_file = doc_file, document_name = doc_name, document_format = doc_format, date_modified = date_mod)
                document.save()

            """ TODO: Check if unique name in regards with the user_id"""
                          
            
        return redirect("viewAllDocs")

    def get(self, request):
        form = UploadDocForm()
        return render(request, self.template_name, {'form': form})

class RenameDocumentView(View):

    def post(self, request):
        id=request.POST.get('id','')
        type=request.POST.get('type','')
        value=request.POST.get('value','')
        print(value)

        if type=="name":
            doc_name = value
    
        Document.objects.filter(document_id=id).update(document_name= doc_name)

        return redirect("viewAllDocs")


