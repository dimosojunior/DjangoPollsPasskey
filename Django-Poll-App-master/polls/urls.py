from django.urls import path
from . import views

#app_name = "polls"

urlpatterns = [
    path('', views.run_uvicorn, name='run_uvicorn'),
    path('register_device/', views.register_device, name='register_device'),
    path('run_command/', views.run_command, name='run_command'),

    path('home/', views.home, name='home'),
    path('OtpPage/', views.OtpPage, name='OtpPage'),

    path('AllElectionCategories/', views.AllElectionCategories, name='AllElectionCategories'),
    path('list/<int:id>/', views.polls_list, name='list'),
    path('list/user/', views.list_by_user, name='list_by_user'),
    path('add/', views.polls_add, name='add'),
    path('edit/<int:poll_id>/', views.polls_edit, name='edit'),
    path('delete/<int:poll_id>/', views.polls_delete, name='delete_poll'),
    path('end/<int:poll_id>/', views.endpoll, name='end_poll'),
    path('edit/<int:poll_id>/choice/add/', views.add_choice, name='add_choice'),
    path('edit/choice/<int:choice_id>/', views.choice_edit, name='choice_edit'),
    path('delete/choice/<int:choice_id>/',
         views.choice_delete, name='choice_delete'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),
]
