from django.contrib import messages
from .models import ProgramModel
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DetailView

# program view
class Program(ListView):
    model = ProgramModel
    template_name = "program/program.html"

# program detail view
class ProgramDetail(DetailView):
    model = ProgramModel
    template_name = "program/detail.html"
    context_object_name = "program"
