from django.urls import path, re_path

from . import views

app_name = 'demostatapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('d/<int:pk>/', views.demo_id, name='demo_id'),
    path('demo/', views.demos, name='demos'),
    re_path(r'^demo/(?P<date__year>[0-9]{4})/(?P<date__month>[0-9]{2})/(?P<date__day>[0-9]{2})/(?P<slug>[\w-]+)/$', views.demo, name='demo'),
    path('organisation/<slug:slug>/', views.OrganisationView.as_view(), name='organisation'),
    path('tag/<slug:tag_slug>/', views.tag, name='tag'),
]
