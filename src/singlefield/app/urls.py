from django.urls import path, include

from . import views

multifield = [
    path('new/', views.CreateBookView.as_view(), name='book-new'),
    path('<int:pk>/delete/', views.DeleteBookView.as_view(), name='book-delete'),
    path('<int:pk>/update/', views.UpdateBookView.as_view(), name='book-edit'),
    path('', views.ListBookView.as_view(), name='book-list'),
]

singlefield = [
    path('new/', views.SingleFieldCreateBookView.as_view(), name='book-new2'),
    path('<int:pk>/delete/', views.SingleFieldDeleteBookView.as_view(), name='book-delete2'),
    path('<int:pk>/<str:fieldname>/', views.SingleFieldBookFieldView.as_view(), name='book-edit-field'),
    path('<int:pk>/<str:fieldname>/update/', views.SingleFieldUpdateBookView.as_view(), name='book-edit2'),
    path('', views.SingleFieldListBookView.as_view(), name='book-list2'),
]

singlefield_htmx_get = [
    path('new/', views.HTMxGetSingleFieldCreateBookView.as_view(), name='book-new3'),
    path('<int:pk>/delete/', views.HTMxGetSingleFieldDeleteBookView.as_view(), name='book-delete3'),
    path('<int:pk>/<str:fieldname>/', views.HTMxGetSingleFieldBookFieldView.as_view(), name='book-edit-field3'),
    path('<int:pk>/<str:fieldname>/update/', views.HTMxGetSingleFieldUpdateBookView.as_view(), name='book-edit3'),
    path('', views.HTMxGetSingleFieldListBookView.as_view(), name='book-list3'),
]

singlefield_htmx_boost = [
    path('new/', views.HTMxBoostSingleFieldCreateBookView.as_view(), name='book-new4'),
    path('<int:pk>/delete/', views.HTMxBoostSingleFieldDeleteBookView.as_view(), name='book-delete4'),
    path('<int:pk>/<str:fieldname>/', views.HTMxBoostSingleFieldBookFieldView.as_view(), name='book-edit-field4'),
    path('<int:pk>/<str:fieldname>/update/', views.HTMxBoostSingleFieldUpdateBookView.as_view(), name='book-edit4'),
    path('', views.HTMxBoostSingleFieldListBookView.as_view(), name='book-list4'),
]

urlpatterns = [
    path("multifield/", include(multifield)),
    path("singlefield/", include(singlefield)),
    path("singlefield-htmx-get/", include(singlefield_htmx_get)),
    path("singlefield-htmx-boost/", include(singlefield_htmx_boost)),
]
