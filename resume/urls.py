from django.urls import path
from resume import views


urlpatterns = [
    path('', views.index, name='index'),
    path('comm_divs/', views.Comm_divListView.as_view(), name='comm_divs'),
    path('comm_div_detail/<int:pk>', views.Comm_divDetailView.as_view(), name='come_div-detail'),

]

urlpatterns += [
    path('comm_div_detail/<int:pk>/update/', views.UpdateComm, name='comm_div_update'),
    path('comm_div_detail/create/', views.CreateComm, name='comm_div_create'),
    path('comm_div_detail/<int:pk>/delete/', views.DeleteComm, name='comm_div_delete'),
]

urlpatterns += [
    path('employee_list/', views.EmployeeList.as_view(), name='employee_list'),
    path('employee_list/<int:pk>/update/', views.EmployeeUpdate, name='employee_update'),
]

urlpatterns += [
    path('education_list/', views.EducationList.as_view(), name='education_list'),
    path('education_list/<int:pk>/update/', views.EducationUpdate, name='education_update'),
]
