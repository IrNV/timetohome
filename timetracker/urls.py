from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import  format_suffix_patterns

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^posts/$', views.post_list, name='post_list'),
    url(r'^posts/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^posts/new/$', views.post_new, name='post_new'),
    url(r'^posts/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^posts/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^register/$', views.RegistrationFormView.as_view(), name="registration"),
    url(r'^login/$', views.LoginFormView.as_view(), name="login"),
    url(r'^logout/$', views.logout_, name="logout"),
    url(r'^timetracker/api/$', views.PostList.as_view()),
]
