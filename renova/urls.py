from django.urls import path
from renova import views

app_name = "renova"

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('about-us/', views.about_us, name='about_us'),
    path('my-logs/', views.my_logs, name='my_logs'),
    path('my-logs/record-log/', views.record_log, name='record_log'),
    path('my-account/', views.my_account, name='my_account'),
    path('groups/', views.groups, name='groups'),
    path('groups/make-group/', views.make_group, name='make_group'),
    path('groups/<slug:group_name_slug>/', views.group, name='group'),
    path('groups/<slug:group_name_slug>/leave', views.leave_group, name='leave_group'),
    path('groups/<slug:group_name_slug>/join', views.join_group, name='join_group'),
    path('groups/<slug:group_slug>/remove_member/<str:username>/', views.remove_member, name='remove_member'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('groups/<slug:group_slug>/edit/', views.edit_group_attributes, name='edit_group_attributes'),
]
