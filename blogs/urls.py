from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
)


app_name = 'blogs'


urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('<int:pk>/', BlogDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='delete'),
]


