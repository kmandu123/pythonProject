from django.urls import path
from resume import views


urlpatterns = [
    path('', views.index, name='index'),
    path('resume_home', views.resume_index, name='resume_index'),
    path('comm_div_list/', views.Comm_divList.as_view(), name='comm_div_list'),
    path('comm_div_list/<int:pk>/update/', views.Comm_divUpdate, name='comm_div_update'),
    path('comm_div_list/create/', views.Comm_divCreate, name='comm_div_create'),
    path('comm_div_list/<int:pk>/delete/', views.Comm_divDelete, name='comm_div_delete'),
]

urlpatterns += [
    path('order_comp_list/', views.Order_compList.as_view(), name='order_comp_list'),
    path('order_comp_list/<int:pk>/update/', views.Order_compUpdate, name='order_comp_update'),
    path('order_comp_list/create/', views.Order_compCreate, name='order_comp_create'),
    path('order_comp_list/<int:pk>/delete/', views.Order_compDelete, name='order_comp_delete'),
]

urlpatterns += [
    path('pjt_list/', views.PjtList.as_view(), name='pjt_list'),
    path('pjt_list/<int:pk>/update/', views.PjtUpdate, name='pjt_update'),
    path('pjt_list/create/', views.PjtCreate, name='pjt_create'),
    path('pjt_list/<int:pk>/delete/', views.PjtDelete, name='pjt_delete'),
    path('pjt_list/order_comp_popup/', views.Order_comp_popup.as_view(), name='order_comp_popup'),
]


urlpatterns += [
    path('education_list/', views.EducationList.as_view(), name='education_list'),
    path('education_list/<int:pk>/update/', views.EducationUpdate, name='education_update'),
    path('education_list/create/', views.EducationCreate, name='education_create'),
    path('education_list/<int:pk>/delete/', views.EducationDelete, name='education_delete'),
]


urlpatterns += [
    path('employee_list/', views.EmployeeList.as_view(), name='employee_list'),
    path('employee_list/<int:pk>/update/', views.EmployeeUpdate, name='employee_update'),
    path('employee_list/create/', views.EmployeeCreate, name='employee_create'),
    path('employee_list/<int:pk>/delete/', views.EmployeeDelete, name='employee_delete'),
    path('employee_list/pjt_popup/', views.Pjt_popup.as_view(), name='pjt_popup'),
]


urlpatterns += [
    path('download_emp/', views.DownloadEmp, name='download_emp'),
]

urlpatterns += [
    path('skill_guide/', views.SkillGuide, name='skill_guide'),
    path('admin_page/', views.AdminPage, name='admin_page'),
    path('admin_page/log_list/', views.LogList.as_view(), name='log_list'),
]

urlpatterns += [
    path('intro_list/', views.IntroList.as_view(), name='intro_list'),
    path('intro_list/<int:pk>/update/', views.IntroUpdate, name='intro_update'),
    path('intro_list/create/', views.IntroCreate, name='intro_create'),
    path('intro_list/<int:pk>/delete/', views.IntroDelete, name='intro_delete'),
]

urlpatterns += [
    path('favorite_location_list/', views.Favorite_locationList.as_view(), name='favorite_location_list'),
    path('favorite_location_list/<int:pk>/update/', views.Favorite_locationUpdate, name='favorite_location_update'),
    path('favorite_location_list/create/', views.Favorite_locationCreate, name='favorite_location_create'),
    path('favorite_location_list/<int:pk>/delete/', views.Favorite_locationDelete, name='favorite_location_delete'),
]