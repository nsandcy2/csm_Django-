# safety_plan/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from core.models import Project, WorkProduct, ProjectWorkProduct
from .models import SafetyPlanDetail

import json

@login_required
def tailor_safety_plan(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    safety_wp = get_object_or_404(WorkProduct, is_safety_plan=True)
    pwp, _ = ProjectWorkProduct.objects.get_or_create(project=project, workproduct=safety_wp)

    # get all other WPs
    other_wps = WorkProduct.objects.exclude(id=safety_wp.id)
    existing_pwps = {pwp.workproduct_id: pwp for pwp in ProjectWorkProduct.objects.filter(project=project)}

    if request.method == "POST":
        if request.user.is_superuser == False:
            messages.error(request, "Only admin can edit Safety Plan")
            return redirect("tailor_safety_plan", project_id=project.id)

        changes_summary = []
        # Tailor other WPs
        for wp in other_wps:
            tailored_out = request.POST.get(f"wp_{wp.id}") == "out"
            if wp.id in existing_pwps:
                p = existing_pwps[wp.id]
                if p.tailored_out != tailored_out:
                    changes_summary.append(f"{wp.name}: {p.tailored_out} -> {tailored_out}")
                    p.tailored_out = tailored_out
                    p.tailored_by = request.user
                    p.tailored_at = timezone.now()
                    p.save()
            else:
                ProjectWorkProduct.objects.create(
                    project=project,
                    workproduct=wp,
                    tailored_out=tailored_out,
                    tailored_by=request.user
                )
                changes_summary.append(f"{wp.name}: created with tailored_out={tailored_out}")

        messages.success(request, "Safety Plan tailored successfully.")
        return redirect("dashboard")

    return render(request, "safety_plan/tailor.html", {
        "project": project,
        "workproducts": [safety_wp] + list(other_wps),
        "existing_pwps": existing_pwps,
        "is_admin": request.user.is_superuser
    })


def get_history(instance):
    logs = []
    for record in instance.history.all().select_related("history_user"):
        changes = []
        prev = record.prev_record
        if prev:
            for field in record._meta.fields:
                field_name = field.name
                if field_name in ["id", "history_id", "history_date", "history_user", "history_type"]:
                    continue
                old_val = getattr(prev, field_name, None)
                new_val = getattr(record, field_name, None)
                if old_val != new_val:
                    changes.append({
                        "field": field_name,
                        "old": old_val,
                        "new": new_val,
                    })
        logs.append({
            "history_date": record.history_date,
            "history_user": record.history_user,
            "history_type": record.get_history_type_display(),
            "changes": changes,
        })
    return sorted(logs, key=lambda x: x["history_date"], reverse=True)

from core.models import ProjectWorkProduct
from .models import SafetyPlanDetail

@login_required
def safetyplan_history(request, project_id):
    # Find the ProjectWorkProduct for the Safety Plan of this project
    pwp = get_object_or_404(ProjectWorkProduct, project_id=project_id, workproduct__is_safety_plan=True)
    
    # Then get the SafetyPlanDetail linked to it
    wp = get_object_or_404(SafetyPlanDetail, project_workproduct=pwp)

    logs = get_history(wp)
    return render(request, "safety_plan/history.html", {"workproduct": wp, "logs": logs})
