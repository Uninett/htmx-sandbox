from django.urls import path, include

from . import views

multifield = [
    path('new/', views.create_view, name='fbv-book-new'),
    path('<int:pk>/delete/', views.delete_view, name='fbv-book-delete'),
    path('<int:pk>/update/', views.update_view, name='fbv-book-edit'),
    path('', views.list_view, name='fbv-book-list'),
]

singlefield = [
    path('new/', views.create_view2, name='fbv-book-new2'),
    path('<int:pk>/delete/', views.delete_view2, name='fbv-book-delete2'),
    path(
        '<int:pk>/<str:fieldname>/', views.get_field_view2, name='fbv-book-edit-field2'
    ),
    path('<int:pk>/<str:fieldname>/update/', views.update_view2, name='fbv-book-edit2'),
    path('', views.list_view2, name='fbv-book-list2'),
]

singlefield_htmx_get = [
    path('new/', views.create_view3, name='fbv-book-new3'),
    path('<int:pk>/delete/', views.delete_view3, name='fbv-book-delete3'),
    path(
        '<int:pk>/<str:fieldname>/', views.get_field_view3, name='fbv-book-edit-field3'
    ),
    path('<int:pk>/<str:fieldname>/update/', views.update_view3, name='fbv-book-edit3'),
    path('', views.list_view3, name='fbv-book-list3'),
]

singlefield_htmx_boost = [
    path('new/', views.create_view4, name='fbv-book-new4'),
    path('<int:pk>/delete/', views.delete_view4, name='fbv-book-delete4'),
    path(
        '<int:pk>/<str:fieldname>/', views.get_field_view4, name='fbv-book-edit-field4'
    ),
    path('<int:pk>/<str:fieldname>/update/', views.update_view4, name='fbv-book-edit4'),
    path('', views.list_view4, name='fbv-book-list4'),
]

urlpatterns = [
    path('multifield/', include(multifield)),
    path('singlefield/', include(singlefield)),
    path('singlefield-htmx-get/', include(singlefield_htmx_get)),
    path('singlefield-htmx-boost/', include(singlefield_htmx_boost)),
]
