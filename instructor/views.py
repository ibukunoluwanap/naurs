from django.contrib import messages
from .models import InstructorModel
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DetailView

# instructor view
class Instructor(ListView):
    model = InstructorModel
    template_name = "instructor/instructor.html"

# instructor detail view
class InstructorDetail(DetailView):
    model = InstructorModel
    template_name = "instructor/detail.html"
    context_object_name = "instructor"