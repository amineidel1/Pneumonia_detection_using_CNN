from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.home,name="home"),
    path('input',views.inputt,name="inputt"),
    path('upload/', views.image_upload_view)
]

urlpatterns += staticfiles_urlpatterns()