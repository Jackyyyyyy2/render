from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_pegawai = models.BooleanField(default=False)
    is_atasan = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}{self.first_name}{self.last_name}'
    

class TujuanDinas(models.Model):
    nama_tujuan = models.CharField(max_length=100)
    kota = models.CharField(max_length=100)
    provinsi = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif')
    
    def __str__(self):
        return f"{self.nama_tujuan}, {self.kota}"

    
class StatusModel(models.Model):
    status_choices = (
        ("Aktif","Aktif"),
        ("Tidak Aktif","Tidak Aktif")
    )
    status=models.CharField(max_length=15,choices=status_choices,default="Aktif") 

    def __str__(self):
        return self.status
    
class KategoriBiaya(models.Model):
    STATUS_CHOICES = (
        ("Aktif", "Aktif"),
        ("Tidak Aktif", "Tidak Aktif")
    )
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Aktif")
    user_create = models.ForeignKey(User, related_name="user_create_kategori_biaya", blank=True, null=True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(User, related_name="user_update_kategori_biaya", blank=True, null=True, on_delete=models.SET_NULL)
    create_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

from django.utils import timezone

def generate_nomor_surat():
    last = PengajuanDinas.objects.all().order_by('id').last()
    if not last:
        return 'SPD-0001'
    nomor = int(last.nomor_surat[4:])
    return f"SPD-{str(nomor + 1).zfill(4)}"

class PengajuanDinas(models.Model):
    STATUS_CHOICES = [
        ('Diajukan', 'Diajukan'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak'),
        ('Selesai', 'Selesai'),
    ]

    pegawai = models.ForeignKey(User, limit_choices_to={'is_pegawai': True}, on_delete=models.CASCADE)
    nomor_surat = models.CharField(max_length=20, default=generate_nomor_surat, editable=False)
    tanggal_berangkat = models.DateField()
    tanggal_kembali = models.DateField()
    tujuan = models.ForeignKey(TujuanDinas, on_delete=models.SET_NULL, null=True)
    keperluan = models.TextField()
    biaya = models.FloatField(default=0.0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Diajukan')
    atasan = models.ForeignKey(User, related_name='pengajuan_disetujui', limit_choices_to={'is_atasan': True}, on_delete=models.SET_NULL, null=True, blank=True)
    tanggal_pengajuan = models.DateTimeField(default=timezone.now)
    tanggal_disetujui = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nomor_surat} - {self.pegawai.first_name} ({self.status})"

    
class BiayaPerjalanan(models.Model):
    pengajuan = models.ForeignKey(PengajuanDinas, on_delete=models.CASCADE, related_name='rincian_biaya')
    kategori = models.ForeignKey(KategoriBiaya, on_delete=models.SET_NULL, null=True)
    keterangan = models.CharField(max_length=200)
    nominal = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.kategori.name} - {self.nominal}"

