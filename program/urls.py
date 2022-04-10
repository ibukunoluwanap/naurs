from django.urls import path
from . import views

urlpatterns = [
    # programs
    path('music/', views.ProgramMusic.as_view(), name='program_music_page'),
    path('fitness/', views.ProgramFitness.as_view(), name='program_fitness_page'),
    path('fine_arts/', views.ProgramFineArts.as_view(), name='program_fine_arts_page'),
    path('dance/', views.ProgramDance.as_view(), name='program_dance_page'),
    path('<int:pk>/', views.ProgramDetail.as_view(), name='program_detail_page'),
    path('enquiry/<int:program_id>/', views.ProgramEnquiry.as_view(), name='program_enquiry_page'),
    # package
    path('package/', views.Package.as_view(), name='package_page'),
    path('package/<int:pk>/', views.PackageDetail.as_view(), name='package_detail_page'),
    # calendar
    path('calendar/', views.CalendarView.as_view(), name='program_calendar'),
]