from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from core.models import Project, WorkProduct, ProjectWorkProduct
from safety_plan.models import SafetyPlanDetail
def home(request):
    return 
 # Redirect to a default project for demo purposes

@login_required
def tailor_safety_plan(request, project_id):
    """
    Admin can tailor the Safety Plan WP and select which WPs to include.
    Regular users can only view.
    """
    project = get_object_or_404(Project, id=project_id)
    safety_wp = get_object_or_404(WorkProduct, is_safety_plan=True)
    project_wp, _ = ProjectWorkProduct.objects.get_or_create(
        project=project,
        workproduct=safety_wp,
        defaults={"tailored_out": False, "tailored_by": request.user}
    )

    # All other WPs
    other_workproducts = WorkProduct.objects.exclude(id=safety_wp.id)
    existing_pwps = {pwp.workproduct_id: pwp for pwp in ProjectWorkProduct.objects.filter(project=project)}

    if request.method == "POST":
        if request.user.role != "admin":
            messages.error(request, "Only admin can edit Safety Plan")
            return redirect("work_products", project_id=project.id)

        # Tailoring Safety Plan WP itself
        tailored_out = request.POST.get(f"wp_{safety_wp.id}") == "out"
        project_wp.tailored_out = tailored_out
        project_wp.tailored_by = request.user
        project_wp.tailored_at = timezone.now()
        project_wp.save()

        # Tailoring other WPs
        for wp in other_workproducts:
            tailored_out = request.POST.get(f"wp_{wp.id}") == "out"
            if wp.id in existing_pwps:
                pwp = existing_pwps[wp.id]
                pwp.tailored_out = tailored_out
                pwp.tailored_by = request.user
                pwp.tailored_at = timezone.now()
                pwp.save()
            else:
                if not tailored_out:
                    ProjectWorkProduct.objects.create(
                        project=project,
                        workproduct=wp,
                        tailored_out=False,
                        tailored_by=request.user
                    )

        messages.success(request, "Safety Plan tailoring saved!")
        return redirect("work_products", project_id=project.id)

    return render(request, "safety_plan/tailor.html", {
        "project": project,
        "workproducts": [safety_wp] + list(other_workproducts),
        "existing_pwps": existing_pwps,
        "is_admin": request.user.role == "admin"
    })
