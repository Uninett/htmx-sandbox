from django.urls import path, include

from . import views


urlpatterns = [
    path('books/', include('singlefield.app.urls')),
    path('', views.HomePageView.as_view()),
]
