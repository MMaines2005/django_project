from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('register', views.register),
    path('landing', views.landing),
    path('landing/add_book', views.book_create),
    path('landing/<int:book_id>', views.oneview),
    path("landing/<int:book_id>/update", views.update),
    path("landing/<int:book_id>/delete", views.delete),
    path("favorite/<int:book_id>", views.favorite),
    path("unfavorite/<int:book_id>", views.unfavorite),
    path('login', views.login),
    path('logout', views.logout),
]