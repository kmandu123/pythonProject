from django.urls import path

from books import views
from resume import views as resume_views

urlpatterns = [
    path('', resume_views.index, name='index'),
    path('author_list/', views.AuthorList.as_view(), name='author_list'),
    path('author_list/<int:pk>/update/', views.AuthorUpdate, name='author_update'),
    path('author_list/create/', views.AuthorCreate, name='author_create'),
    path('author_list/<int:pk>/delete/', views.AuthorDelete, name='author_delete'),
]

