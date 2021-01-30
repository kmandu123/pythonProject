from django.urls import path
from resume import views


urlpatterns = [
    path('', views.index, name='index'),
    path('comm_divs/', views.Comm_divListView.as_view(), name='comm_divs'),
    path('comm_div_detail/<int:pk>', views.Comm_divDetailView.as_view(), name='come_div-detail'),

]

urlpatterns += [
    path('comm_div_detail/<int:pk>/update/', views.UpdateComm_div, name='comm_div_update'),
]

urlpatterns += [
     path('comm_div_detail/create/', views.CreateComm_div, name='comm_div_create'),
]

urlpatterns += [
    path('comm_div_detail/<int:pk>/delete/', views.DeleteComm_div, name='comm_div_delete'),
]
