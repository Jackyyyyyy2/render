from django.urls import path
from api.views import (RegisterUserAPIView,LoginView,TujuanDinasListApiView,TujuanDinasDetailApiView,KategoriBiayaListApiView,KategoriBiayaDetailApiView,PengajuanDinasListApiView,PengajuanDinasDetailApiView,)

app_name = 'api'

urlpatterns = [
    # Auth
    path('api/register', RegisterUserAPIView.as_view(), name='register'),
    path('api/login', LoginView.as_view(), name='login'),

    # Tujuan Dinas
    path('api/tujuan', TujuanDinasListApiView.as_view(), name='tujuan-list'),
    path('api/tujuan/<int:id>', TujuanDinasDetailApiView.as_view(), name='tujuan-detail'),

    # Kategori Biaya
    path('api/kategori', KategoriBiayaListApiView.as_view(), name='kategori-list'),
    path('api/kategori/<int:id>', KategoriBiayaDetailApiView.as_view(), name='kategori-detail'),

    # Pengajuan Dinas
    path('api/pengajuan', PengajuanDinasListApiView.as_view(), name='pengajuan-list'),
    path('api/pengajuan/<int:id>', PengajuanDinasDetailApiView.as_view(), name='pengajuan-detail'),
]
