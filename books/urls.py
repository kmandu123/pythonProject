from django.urls import path

from books import views
from resume import views as resume_views

urlpatterns = [
    path('', resume_views.index, name='index'),
    path('author_list/', views.AuthorList.as_view(), name='author_list'),
]

