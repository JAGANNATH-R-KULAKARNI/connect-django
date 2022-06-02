from django.urls import path
from . import views

urlpatterns=[
    path('',views.home_page,name='home_page'),
        path('login',views.login_page,name='login_page'),
           path('profile',views.profile_page,name='profile_page'),
           path('profileedit',views.profileedit,name='profileedit'),
           path('profilelikes/<post_id>',views.profilelikes,name='profilelikes'),
           path('homelikes/<post_id>',views.homelikes,name='home_likes'),
           path('follow/<username>',views.follow_person,name='follow_person'),
           path('comments',views.comments_page,name='comments'),
           path('signup',views.signup_page,name='signup_page'),
      path('logout',views.log_out,name='logout_page'),
]