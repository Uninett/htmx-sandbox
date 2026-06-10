from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('', include('singlefield.app.urls')),
] + debug_toolbar_urls()
