from django.shortcuts import render
# Create your views here.

def notes_list(request):
    return render(request,'notesko.html')

def upload_notes(request):
    return render(request,'upload.html')