from django.shortcuts import render,redirect

# Create your views here.

def index(request,request_id):
   
    return render(request, "wp4/index.html")  # Django uses URL names, not function names`
 