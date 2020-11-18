from django.urls import path

from materials import views

app_name = 'materials'

urlpatterns = [
    path('<int:material_id>/attributes/', views.AttributesListAPIView.as_view(), name='attributes'),
    path('recyclers/', views.RecyclerListAPIView.as_view(), name='recyclers'),
]
