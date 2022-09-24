from django.urls import path
from . import views

urlpatterns = [
    # path('applicant/<slug:uid>',views.ApplicantDetails.as_view()),
    path('create/', views.ApplicantCreateView.as_view()),
    path('detail/<uid>', views.ApplicantDetailsView.as_view()),
    path('detail/v2/<uid>', views.ApplicantDetailsViewV2.as_view()),
    path('update/<uid>', views.ApplicantUpdateView.as_view()), 
    path('delete/<uid>', views.ApplicantDeleteView.as_view()), 
    path('profile/<uid>', views.ApplicantGetUpateDeleteView.as_view()),
    path('search/', views.ApplicantSearchView.as_view()),
    path('search/custom/', views.search),
    path('app_status/<uid>', views.ApplicantStatus.as_view()),


]
