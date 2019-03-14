from django.urls import path, re_path

from . import views

app_name = 'demostat'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('about/', views.AboutView, name='about'),
    path('d/<int:demo_id>/', views.demo_id, name='demo_id'),
    path('demo/', views.demos, name='demos'),
    re_path(r'^demo/(?P<date__year>[0-9]{4})/$', views.demos_year, name='demos_year'),
    re_path(r'^demo/(?P<date__year>[0-9]{4})/(?P<date__month>[0-9]{2})/$', views.demos_month, name='demos_month'),
    re_path(r'^demo/(?P<date__year>[0-9]{4})/(?P<date__month>[0-9]{2})/(?P<date__day>[0-9]{2})/$', views.demos_day, name='demo_day'),
    re_path(r'^demo/(?P<date__year>[0-9]{4})/(?P<date__month>[0-9]{2})/(?P<date__day>[0-9]{2})/(?P<slug>[\w-]+)/$', views.demo, name='demo'),
    path('organisation/<slug:slug>/', views.OrganisationView, name='organisation'),
    path('tag/<slug:tag_slug>/', views.tag, name='tag'),
]
