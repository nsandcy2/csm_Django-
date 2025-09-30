from django.shortcuts import render,redirect

# Create your views here.

def index(request,project_id):
   
    return render(request, "wp3/index.html")  # Django uses URL names, not function names`
 