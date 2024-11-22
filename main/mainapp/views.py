from django.shortcuts import render
from .forms import AstronomyBlogPostForm
from .models import AstronomyBlogPost
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, HttpResponseRedirect, HttpResponse

def home_view(request):
    context ={}
    return render(request, "mainapp/home_view.html", context) 

def list_view(request):
    context ={}
    context["blog_posts"] = AstronomyBlogPost.objects.all().order_by('-id')
    return render(request, "mainapp/list_view.html", context) 


@login_required
def create_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = AstronomyBlogPostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/list")
         
    context['form']= form
    return render(request, "mainapp/create_view.html", context)
