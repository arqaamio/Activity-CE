#!/usr/bin/python3
# -*- coding: utf-8 -*-

import uuid
from django.db import models
from workflow.models import Program, Office, Stakeholder, Site
from formlibrary.models import Case

class StartEndDates(models.Model):
    """
    Abstract Base Class to implement start/end dates fields
    """
    # TODO move to its own place
    # TODO Check the start_date < end_date and throw adequate error if else
    start_date = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class Service(StartEndDates):
    """
    Abstract base class for all kinds of offered services.
    Spec: https://github.com/hikaya-io/activity/issues/412
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=550, null=True, blank=True)
    program = models.OneToOneField(
        Program, null=True, blank=True, on_delete=models.SET_NULL)
    office = models.ForeignKey(
        Office, null=True, blank=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(
        Site, null=True, blank=True, on_delete=models.SET_NULL)
    implementer = models.OneToOneField(
        Stakeholder, null=True, blank=True, on_delete=models.SET_NULL)
    cases = models.ForeignKey(
        Case, null=True, blank=True, on_delete=models.SET_NULL)
    form_verified_by = models.CharField(max_length=255, null=True, blank=True)
    form_filled_by = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
