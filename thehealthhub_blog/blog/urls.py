from django.urls import path
from .views import blog_index, blog_detail, blog_category, login_view
# from .views import create_post, post_detail
from . import views

urlpatterns = [
    # path('create/', create_post, name='create_post'),
    # path('post/<slug:slug>/', post_detail, name='post_detail'),
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path('login/', login_view, name='login_view'),
]