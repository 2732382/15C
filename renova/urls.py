from django.urls import path
from renova import views

app_name = "renova"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('faq/', views.faq, name='faq'),
    path('about-us/', views.about_us, name='about_us'),
    path('my-logs/', views.my_logs, name='my_logs'),
    path('my-logs/record-log/', views.record_log, name='record_log'),
    path('my-account/', views.my_account, name='my_account'),
    path('groups/', views.groups, name='groups'),
    path('groups/<slug:group_name_slug>/', views.group_detail, name='group_detail'),
    path('groups/make-group/', views.make_group, name='make_group'),
]