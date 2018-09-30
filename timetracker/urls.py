from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    #url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^register/$', views.RegisterFormView.as_view(), name="register"),
    url(r'^login/$', views.LoginFormView.as_view(), name="login"),
    url(r'^logout/$', views.logout_, name="logout"),
]
