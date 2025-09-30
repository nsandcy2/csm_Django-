from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WP1Detail
from safety_plan.views import get_history  # reuse history function
# Create your views here.

def index(request,project_id):
   
    return render(request, "wp1/index.html")  # Django uses URL names, not function names`


@login_required
def history_view(request, pk):
    wp = get_object_or_404(WP1Detail, pk=pk)
    logs = get_history(wp)
    return render(request, "wp1/history.html", {"workproduct": wp, "logs": logs})
