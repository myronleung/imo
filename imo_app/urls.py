from django.conf.urls import url

from . import views

app_name = 'imo_app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^your_posts/$', views.your_posts, name = 'your_posts'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name = 'detail'),
    url(r'^view_registration/$', views.view_registration, name='view_registration'),
    url(r'^submit_registration/$', views.submit_registration, name='submit_registration'),
    url(r'^view_login/$', views.view_login, name='view_login'),
    url(r'^submit_login/$', views.submit_login, name = 'submit_login'),
    url(r'^user_logout/$', views.user_logout, name = 'user_logout'),
    url(r'^view_newentry/$', views.view_newentry, name = 'view_newentry'),
    url(r'^submit_newentry/$', views.submit_newentry, name = 'submit_newentry'),
    url(r'^(?P<question_id>[0-9]+)/submit_vote/$', views.submit_vote, name = 'submit_vote'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name = 'results'),
    url(r'^(?P<id>\d+)/edit/$', views.edit, name = 'edit'),
    url(r'^(?P<question_id>[0-9]+)/add_comment/$', views.add_comment, name = 'add_comment'),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^faq/$', views.faq, name = 'faq'),
    url(r'^profile/$', views.profile, name = 'profile'),
    url(r'^search/', views.search, name = 'search'),
]
