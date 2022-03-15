from django.views.generic import ListView
from about.models import AboutModel

# about list view
class About(ListView):
    model = AboutModel
    login_url = 'login_page'
    template_name = "about/about.html"
