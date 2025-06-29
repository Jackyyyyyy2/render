from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from pos_app.models import (User,TujuanDinas,KategoriBiaya,PengajuanDinas,StatusModel)
from api.serializers import (RegisterUserSerializer,LoginSerializer,TujuanDinasSerializer,KategoriBiayaSerializer,PengajuanDinasSerializer)
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login,logout as django_logout
from django.http import HttpResponse , JsonResponse
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from .paginators import CustomPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.contrib.auth import authenticate


class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'User berhasil didaftarkan.',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Username atau password salah'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TujuanDinasListApiView(APIView):
    def get(self, request):
        tujuan = TujuanDinas.objects.all()
        serializer = TujuanDinasSerializer(tujuan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TujuanDinasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Tujuan berhasil ditambahkan.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# GET by ID, PUT, DELETE
class TujuanDinasDetailApiView(APIView):
    def get_object(self, id):
        try:
            return TujuanDinas.objects.get(id=id)
        except TujuanDinas.DoesNotExist:
            return None

    def get(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TujuanDinasSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TujuanDinasSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Data berhasil diperbarui.',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({'message': 'Data berhasil dihapus.'}, status=status.HTTP_200_OK)


class KategoriBiayaListApiView(APIView):
    def get(self, request):
        kategori = KategoriBiaya.objects.all()
        serializer = KategoriBiayaSerializer(kategori, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = KategoriBiayaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Kategori berhasil ditambahkan.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KategoriBiayaDetailApiView(APIView):
    def get_object(self, id):
        try:
            return KategoriBiaya.objects.get(id=id)
        except KategoriBiaya.DoesNotExist:
            return None

    def get(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = KategoriBiayaSerializer(obj)
        return Response(serializer.data)

    def put(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = KategoriBiayaSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data berhasil diperbarui.', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({'message': 'Data berhasil dihapus.'}, status=status.HTTP_200_OK)


class PengajuanDinasListApiView(APIView):
    def get(self, request):
        pengajuan = PengajuanDinas.objects.all()
        serializer = PengajuanDinasSerializer(pengajuan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PengajuanDinasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Pengajuan berhasil dikirim.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET by ID, PUT, DELETE
class PengajuanDinasDetailApiView(APIView):
    def get_object(self, id):
        try:
            return PengajuanDinas.objects.get(id=id)
        except PengajuanDinas.DoesNotExist:
            return None

    def get(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PengajuanDinasSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PengajuanDinasSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid():
            # Otomatis isi tanggal disetujui kalau status berubah ke Disetujui
            if request.data.get("status") == "Disetujui" and obj.tanggal_disetujui is None:
                serializer.save(tanggal_disetujui=timezone.now())
            else:
                serializer.save()

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Data berhasil diperbarui.',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({'message': 'Pengajuan berhasil dihapus.'}, status=status.HTTP_200_OK)