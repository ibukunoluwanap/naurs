from django.views.generic import ListView
from home.models import ListingModel

# home list view
class Home(ListView):
    model = ListingModel
    login_url = 'login_page'
    template_name = "home/home.html"
