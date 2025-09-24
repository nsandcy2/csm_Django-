from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
import io
import re
from datetime import datetime

from .models import ChangeRequest, ImpactAnalysis
from .forms import ChangeRequestForm, ImpactAnalysisForm

# Configuration
work_products = [
    {"name": "Change Request ID", "input_type": "text"},
    {"name": "Start Date", "input_type": "date"},
    {"name": "Phase", "input_type": "select", "options": [
        "Change Request Description Phase",
        "Impact Analysis Phase",
        "Dependent Work Product Analysis Phase",
        "Verification Phase",
        "Closure"
    ]},
    {"name": "End Date", "input_type": "date"},
    {"name": "Summary of Change", "input_type": "textarea"},
]

additional_fields = [
    {"name": "Responsible Person", "input_type": "text"},
    {"name": "Document subject to change", "input_type": "text"},
    {"name": "Current Version", "input_type": "text"},
    {"name": "Configuration of the document", "input_type": "text"},
    {
        "name": "Type of Change Request",
        "input_type": "checkbox",
        "options": ["Error Resolution", "Adaption", "Elimination", "Enhancement", "Prevention"]
    },
    {"name": "Change Type", "input_type": "select", "options": ["Temporary", "Permanent"]},
    {"name": "Change Period (if Temporary)", "input_type": "daterange"},
    {"name": "Change Description", "input_type": "textarea"},
    {"name": "Reason for Change", "input_type": "textarea"},
    {"name": "Phase Status", "input_type": "select", "options": ["Open", "Closed"]},
]

impact_analysis_fields = [
    {"name": "Change Request ID", "input_type": "text", "readonly": True},
    {"name": "Start Date", "input_type": "date"},
    {"name": "Due Date", "input_type": "date"},
    {"name": "Responsible Person", "input_type": "text"},
    {"name": "Change Severity", "input_type": "select", "options": ["Major", "Minor"]},
    {"name": "Impact on Functional Safety", "input_type": "select", "options": ["Yes", "No"]},
    {"name": "Justification", "input_type": "textarea"},
    {"name": "Change Request Status", "input_type": "select", "options": ["Approved", "Rejected", "Delayed"]},
    {"name": "Rationale (if Rejected/Delayed)", "input_type": "textarea"},
    {"name": "Phase Status", "input_type": "select", "options": ["Open", "Closed"]}
]

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def parse_date(value):
    if value in ('', 'N/A', None):
        return None
    return value

def index(request):
    return render(request, 'crms/select_template.html')

def new_request(request):
    change_request_id = request.GET.get('change_request_id')
    saved_data = {}

    if request.method == 'POST':
        form_action = request.POST.get('action')
        values = {}

        for i, wp in enumerate(work_products, start=1):
            key = f'value{i}'
            values[wp['name']] = request.POST.get(key, '').strip()

        cr_id = request.POST.get('change_request_id', '').strip()

        if not cr_id:
            cr_id = f"CR{datetime.now().strftime('%Y%m%d%H%M%S')}"

        try:
            with transaction.atomic():
                cr, created = ChangeRequest.objects.get_or_create(
                    change_request_id=cr_id,
                    defaults={
                        'start_date': values.get("Start Date"),
                        'end_date': values.get("End Date"),
                        'phase': values.get("Phase"),
                        'summary_of_change': values.get("Summary of Change"),
                    }
                )

                if not created:
                    cr.start_date = values.get("Start Date")
                    cr.end_date = values.get("End Date")
                    cr.phase = values.get("Phase")
                    cr.summary_of_change = values.get("Summary of Change")
                    cr.save()

                saved_data = {
                'change_request_id': cr.change_request_id,
                'start_date': cr.start_date or '',
                'end_date': cr.end_date or '',
                'phase': cr.phase or '',
                'summary_of_change': cr.summary_of_change or ''
                                }

                if form_action == 'Next':
                    return redirect('new_request_step2', change_request_id=cr.change_request_id)
                elif form_action == 'Save':
                    messages.success(request, "Saved successfully.")

        except Exception as e:
            messages.error(request, f"Error saving data: {str(e)}")

    elif change_request_id:
        try:
            cr = ChangeRequest.objects.get(change_request_id=change_request_id)
            saved_data = {
                "Change Request ID": cr.change_request_id,
                "Start Date": cr.start_date or '',
                "End Date": cr.end_date or '',
                "Phase": cr.phase or '',
                "Summary of Change": cr.summary_of_change or ''
            }
        except ChangeRequest.DoesNotExist:
            messages.error(request, f"Change Request '{change_request_id}' not found")

    return render(request, 'crms/first_template.html', {
        'saved_data': saved_data,
        'work_products': work_products
    })

def new_request_step2(request, change_request_id):
    try:
        cr = ChangeRequest.objects.get(change_request_id=change_request_id)
        print(cr)
    except ChangeRequest.DoesNotExist:
        messages.error(request, f"Change Request '{change_request_id}' not found")
        return redirect('index')

    if request.method == 'POST':
        try:
            for field in additional_fields:
                key = field['name'].replace(' ', '_').lower()
                if field['input_type'] == 'checkbox':
                    values = request.POST.getlist(field['name'])
                    setattr(cr, key, ','.join(values))
                else:
                    setattr(cr, key, request.POST.get(field['name'], '').strip())

            cr.change_period_from = parse_date(request.POST.get('change_period_from'))
            cr.change_period_to = parse_date(request.POST.get('change_period_to'))
            cr.email_ids = request.POST.get('email', '').strip()

            if 'file' in request.FILES:
                file = request.FILES['file']
                cr.uploaded_file_name = file.name
                cr.uploaded_file_data = file.read()
                cr.uploaded_file_type = file.content_type

            cr.save()
            messages.success(request, "Saved successfully.")

            if 'send_email' in request.POST:
                email_input = request.POST.get('email', '')
                if email_input:
                    email_list = [e.strip() for e in email_input.replace('\n', ',').split(',') if e.strip()]
                    invalid_emails = [email for email in email_list if not is_valid_email(email)]
                    
                    if invalid_emails:
                        messages.error(request, f"Invalid email(s): {', '.join(invalid_emails)}")
                    else:
                        try:
                            send_change_request_email(cr, email_list)
                            messages.success(request, "Email sent successfully.")
                        except Exception as e:
                            messages.error(request, f"Failed to send email: {str(e)}")

        except Exception as e:
            messages.error(request, f"Error saving data: {str(e)}")

    return render(request, 'crms/second_template.html', {
        'change_request': cr,
        'additional_fields': additional_fields
    })

def send_change_request_email(change_request, recipients):
    subject = f"Change Request Notification - {change_request.change_request_id}"
    body = f"Change Request ID: {change_request.change_request_id}\n\nDetails:\n"
    
    for field in change_request._meta.fields:
        if field.name != 'file':
            value = getattr(change_request, field.name)
            formatted_name = field.name.replace('_', ' ').title()
            body += f"{formatted_name}: {value}\n"

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
    )

    if change_request.uploaded_file_data:
        email.attach(
            filename=change_request.uploaded_file_name,
            content=change_request.uploaded_file_data,
            mimetype=change_request.uploaded_file_type
        )

    email.send()

def existing_change_request(request):
    if request.method == 'POST':
        cr_id = request.POST.get('change_request_id')
        if not cr_id:
            messages.error(request, "Please enter a Change Request ID.")
        else:
            try:
                cr = ChangeRequest.objects.get(change_request_id=cr_id)
                return redirect('existing_change_request_step1', change_request_id=cr_id)
            except ChangeRequest.DoesNotExist:
                messages.error(request, "Change Request ID not found.")
    
    return render(request, 'crms/existing_lookup.html')

def existing_change_request_step1(request, change_request_id):
    try:
        cr = ChangeRequest.objects.get(change_request_id=change_request_id)
    except ChangeRequest.DoesNotExist:
        messages.error(request, f"Change Request '{change_request_id}' not found")
        return redirect('existing_change_request')

    saved_data = {
        "Change Request ID": cr.change_request_id,
        "Start Date": cr.start_date or '',
        "End Date": cr.end_date or '',
        "Phase": cr.phase or '',
        "Summary of Change": cr.summary_of_change or ''
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        cr.start_date = request.POST.get('value1') or None
        cr.end_date = request.POST.get('value2') or None
        cr.phase = request.POST.get('value3') or ''
        cr.summary_of_change = request.POST.get('value4') or ''
        cr.save()

        if action == 'Next':
            return redirect('existing_change_request_step2', change_request_id=cr.change_request_id)

        messages.success(request, "Saved successfully.")

    return render(request, 'crms/first_template.html', {
        'saved_data': saved_data,
        'work_products': work_products
    })

def existing_change_request_step2(request, change_request_id):
    try:
        cr = ChangeRequest.objects.get(change_request_id=change_request_id)
    except ChangeRequest.DoesNotExist:
        messages.error(request, f"Change Request '{change_request_id}' not found")
        return redirect('existing_change_request')

    if request.method == 'POST':
        try:
            for field in additional_fields:
                key = field['name'].replace(' ', '_').lower()
                if field['input_type'] == 'checkbox':
                    values = request.POST.getlist(field['name'])
                    setattr(cr, key, ','.join(values))
                else:
                    setattr(cr, key, request.POST.get(field['name'], '').strip())

            cr.change_period_from = request.POST.get('change_period_from')
            cr.change_period_to = request.POST.get('change_period_to')
            cr.email_ids = request.POST.get('email', '').strip()

            if 'file' in request.FILES:
                file = request.FILES['file']
                cr.uploaded_file_name = file.name
                cr.uploaded_file_data = file.read()
                cr.uploaded_file_type = file.content_type

            cr.save()
            messages.success(request, "Second page saved successfully.")

        except Exception as e:
            messages.error(request, f"Error saving data: {str(e)}")

    return render(request, 'crms/second_template.html', {
        'change_request': cr,
        'additional_fields': additional_fields
    })

def download_db_file(request, cr_id):
    try:
        cr = ChangeRequest.objects.get(change_request_id=cr_id)
        if cr.uploaded_file_data:
            return FileResponse(
                io.BytesIO(cr.uploaded_file_data),
                as_attachment=True,
                filename=cr.uploaded_file_name
            )
        else:
            messages.error(request, "No file found for this record.")
            return redirect('existing_change_request_step2', change_request_id=cr_id)
    except ChangeRequest.DoesNotExist:
        messages.error(request, "Change Request not found.")
        return redirect('index')

def impact_analysis(request):
    cr_id = request.POST.get('change_request_id') or request.GET.get('change_request_id')
    if not cr_id:
        messages.error(request, "Change Request ID is required")
        return redirect('index')

    try:
        cr = ChangeRequest.objects.get(change_request_id=cr_id)
    except ChangeRequest.DoesNotExist:
        messages.error(request, f"Change Request '{cr_id}' not found")
        return redirect('index')

    try:
        impact = ImpactAnalysis.objects.get(change_request=cr)
    except ImpactAnalysis.DoesNotExist:
        impact = ImpactAnalysis(change_request=cr)

    if request.method == 'POST':
        impact.start_date = request.POST.get('start_date') or None
        impact.due_date = request.POST.get('due_date') or None
        impact.responsible_person = request.POST.get('responsible_person', '').strip()
        impact.change_severity = request.POST.get('change_severity', '').strip()
        impact.impact_on_functional_safety = request.POST.get('impact_on_functional_safety', '').strip()
        impact.justification = request.POST.get('justification', '').strip()
        impact.change_request_status = request.POST.get('change_request_status', '').strip()
        impact.rationale_if_rejected_delay = request.POST.get('rationale_if_rejected_delay', '').strip()
        impact.phase_status = request.POST.get('phase_status', '').strip()
        impact.email_ids = request.POST.get('email_id', '').strip()

        impact.save()
        messages.success(request, "Impact analysis saved successfully.")

        if 'send_email' in request.POST:
            email_input = request.POST.get('email_id', '')
            if email_input:
                email_list = [e.strip() for e in email_input.split(',') if e.strip()]
                invalid_emails = [email for email in email_list if not is_valid_email(email)]
                
                if invalid_emails:
                    messages.error(request, f"Invalid email(s): {', '.join(invalid_emails)}")
                else:
                    try:
                        send_impact_analysis_email(impact, email_list)
                        messages.success(request, f"Email sent to {', '.join(email_list)}")
                    except Exception as e:
                        messages.error(request, f"Failed to send email: {str(e)}")

        if 'next_form' in request.POST:
            return redirect('work_product_analysis', change_request_id=cr_id)

    return render(request, 'crms/impact_analysis.html', {
        'impact': impact
    })

def send_impact_analysis_email(impact_analysis, recipients):
    subject = f"Impact Analysis Notification - {impact_analysis.change_request.change_request_id}"
    body = f"""
Impact Analysis has been updated for Change Request ID: {impact_analysis.change_request.change_request_id}

Details:
- Start Date: {impact_analysis.start_date}
- Due Date: {impact_analysis.due_date}
- Responsible Person: {impact_analysis.responsible_person}
- Change Severity: {impact_analysis.change_severity}
- Impact on Functional Safety: {impact_analysis.impact_on_functional_safety}
- Change Request Status: {impact_analysis.change_request_status}

Please log in to the system to review the complete details.

Regards,  
Change Management Team
"""

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
    )
    email.send()

def auto_checklist(request):
    cr_id = request.GET.get('change_request_id')
    if not cr_id:
        messages.error(request, "Change Request ID is required")
        return redirect('index')

    try:
        cr = ChangeRequest.objects.get(change_request_id=cr_id)
    except ChangeRequest.DoesNotExist:
        messages.error(request, f"Change Request ID '{cr_id}' not found")
        return redirect('index')

    checks = []

    # Checklist logic
    formatted = cr.change_request_id.startswith("CR") and cr.change_request_id[2:].isdigit()
    checks.append(("Is the Change Request ID properly formatted?", "Pass" if formatted else "Fail"))

    try:
        from datetime import datetime
        start = datetime.strptime(cr.start_date, "%Y-%m-%d") if cr.start_date else None
        end = datetime.strptime(cr.end_date, "%Y-%m-%d") if cr.end_date else None
        date_check = start and end and end >= start
        checks.append(("Is the End Date after the Start Date?", "Pass" if date_check else "Fail"))
    except Exception:
        checks.append(("Is the End Date after the Start Date?", "Fail"))

    doc_uploaded = cr.uploaded_file_name is not None
    checks.append(("Is the document uploaded (hyperlinked)?", "Pass" if doc_uploaded else "Fail"))

    import re
    decimal_pattern = re.compile(r'^\d+(\.\d+)?$')
    is_decimal = bool(decimal_pattern.match(cr.current_version or ""))
    checks.append(("Is the Version in correct decimal format?", "Pass" if is_decimal else "Fail"))

    required_fields = [cr.start_date, cr.end_date, cr.phase, cr.summary_of_change, cr.current_version]
    all_filled = all(str(f).strip() for f in required_fields if f is not None)
    checks.append(("Are all mandatory fields in Change Request filled?", "Pass" if all_filled else "Fail"))

    return render(request, 'crms/checklist.html', {
        'cr_id': cr_id,
        'checks': checks
    })