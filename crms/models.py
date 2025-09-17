from django.db import models
import re
from datetime import datetime

class ChangeRequest(models.Model):
    PHASE_CHOICES = [
        ("Change Request Description Phase", "Change Request Description Phase"),
        ("Impact Analysis Phase", "Impact Analysis Phase"),
        ("Dependent Work Product Analysis Phase", "Dependent Work Product Analysis Phase"),
        ("Verification Phase", "Verification Phase"),
        ("Closure", "Closure"),
    ]
    
    CHANGE_TYPE_CHOICES = [
        ("Temporary", "Temporary"),
        ("Permanent", "Permanent"),
    ]
    
    PHASE_STATUS_CHOICES = [
        ("Open", "Open"),
        ("Closed", "Closed"),
    ]
    
    change_request_id = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(null=True, blank=True)
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES, blank=True)
    end_date = models.DateField(null=True, blank=True)
    summary_of_change = models.TextField(blank=True)

    responsible_person = models.CharField(max_length=255, blank=True)
    document_subject_to_change = models.CharField(max_length=255, blank=True)
    current_version = models.CharField(max_length=255, blank=True)
    configuration_of_the_document = models.CharField(max_length=255, blank=True)
    type_of_change_request = models.CharField(max_length=255, blank=True)
    change_type = models.CharField(max_length=50, choices=CHANGE_TYPE_CHOICES, blank=True)
    change_period_from = models.DateField(null=True, blank=True)
    change_period_to = models.DateField(null=True, blank=True)
    change_description = models.TextField(blank=True)
    reason_for_change = models.TextField(blank=True)
    phase_status = models.CharField(max_length=50, choices=PHASE_STATUS_CHOICES, blank=True)
    email_ids = models.TextField(blank=True)

    uploaded_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.change_request_id:
            self.change_request_id = f"CR{datetime.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.change_request_id


class ImpactAnalysis(models.Model):
    CHANGE_SEVERITY_CHOICES = [
        ("Major", "Major"),
        ("Minor", "Minor"),
    ]
    
    IMPACT_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]
    
    STATUS_CHOICES = [
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Delayed", "Delayed"),
    ]
    
    change_request = models.OneToOneField(ChangeRequest, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    responsible_person = models.CharField(max_length=100, blank=True)
    change_severity = models.CharField(max_length=50, choices=CHANGE_SEVERITY_CHOICES, blank=True)
    impact_on_functional_safety = models.CharField(max_length=50, choices=IMPACT_CHOICES, blank=True)
    justification = models.TextField(blank=True)
    change_request_status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True)
    rationale_if_rejected_delay = models.TextField(blank=True)
    phase_status = models.CharField(max_length=100, blank=True)
    email_ids = models.TextField(blank=True)

    def __str__(self):
        return f"Impact Analysis for {self.change_request.change_request_id}"