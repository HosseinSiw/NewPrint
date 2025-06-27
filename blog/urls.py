from django.urls import path
from . import views as V


app_name = 'blog'


urlpatterns = [
    path('', V.PostListView.as_view(), name='blogs'),
    path('<slug:slug>/', V.PostDetailView.as_view(), name='blog_details'),
]
