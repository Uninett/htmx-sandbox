from django.urls import path, include

from . import views


urlpatterns = [
    path('cbv/', include('singlefield.app.cbv.urls')),
    path('fbv/', include('singlefield.app.fbv.urls')),
    path('', views.HomePageView.as_view()),
]
