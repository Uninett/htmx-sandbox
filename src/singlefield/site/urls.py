from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls

from . import views


urlpatterns = [
    path('books/', include('singlefield.app.urls')),
    path('', views.HomePageView.as_view()),
] + debug_toolbar_urls()
