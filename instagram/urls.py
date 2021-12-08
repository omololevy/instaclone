from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_picture,home_page,view_post,profile,update_profile,add_comment,like_post,follow,unfollow,search_results,user_profile,signup_view
import django.contrib.auth.urls 
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views  as auth_views

app_name ="instagram"


urlpatterns=[
 
path('',home_page,name='home'),
path('upload/',upload_picture, name='upload'),
path('post/<int:pk>',view_post, name='view_post'),
path('profile/<str:username>',profile, name='profile'),
path('update_profile/<int:id>',update_profile, name='update_profile'),
path('accounts/', include('django.contrib.auth.urls')),
path('signup/', signup_view, name='signup'),
path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(next_page = '/')),
path('follow/<int:id>',follow, name='follow'),
path('unfollow/<int:id>',unfollow, name='unfollow'),
path('search/',search_results, name='search_results'),
path('user_profile/<str:username>',user_profile, name='user_profile'),
path('add_comment/<int:post_id>',add_comment, name='add_comment'),
path('like_post/<int:post_id>',like_post, name='like_post'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
