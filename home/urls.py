from django.urls import path
from . import views as V


app_name = 'home'

urlpatterns = [
    path('', V.HomeView.as_view(), name='index'),
    # path("about/", V.AboutView.as_view(), name='about'),
    path("projects/", V.ProjectsView.as_view(), name='projects'),
]