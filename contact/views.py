from django.views.generic import View
from django.shortcuts import render

# contact list view
class Contact(View):
    template_name = "contact/contact.html"
    def get(self, request):
        return render(request, self.template_name)
