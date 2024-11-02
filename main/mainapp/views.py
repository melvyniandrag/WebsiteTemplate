from django.shortcuts import render

def home_view(request):
    context ={}
    return render(request, "mainapp/home_view.html", context) 

def list_view(request):
    context ={}
    return render(request, "mainapp/list_view.html", context) 


def create_view(request):
    context ={}
    return render(request, "mainapp/create_view.html", context) 
