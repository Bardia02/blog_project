from django.urls import path
from . import views


app_name="blog"
urlpatterns=[
    path("detail/<slug:slug>",views.ArticleDetailView.as_view(),name="detail"),
    path("list",views.posts_list,name="list"),
    path("category/<int:pk>",views.category_detail,name="category_list"),
    path("search",views.search,name="search_article"),
    path("contact_us",views.ContactUsView.as_view(),name="contact_us"),
    path("list2",views.ArticleList.as_view(),name="class_list"),
    path("like/<slug:slug>/<int:pk>",views.like,name="like")
]