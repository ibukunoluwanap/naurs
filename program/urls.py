from django.urls import path
from . import views

urlpatterns = [
    path('', views.Program.as_view(), name='program_page'),
    path('<int:pk>/', views.ProgramDetail.as_view(), name='program_detail_page'),
]