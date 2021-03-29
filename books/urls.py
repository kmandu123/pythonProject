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

urlpatterns += [
    path('book_list/', views.BookList.as_view(), name='book_list'),
    path('book_list/<int:pk>/update/', views.BookUpdate, name='book_update'),
    path('book_list/create/', views.BookCreate, name='book_create'),
    path('book_list/<int:pk>/delete/', views.BookDelete, name='book_delete'),
]

urlpatterns += [
    path('best_book_list/', views.Best_bookList.as_view(), name='best_book_list'),
]
