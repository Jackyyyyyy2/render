from django.contrib import admin
from .models import User, TujuanDinas, StatusModel, KategoriBiaya, PengajuanDinas, BiayaPerjalanan

admin.site.register(User)
admin.site.register(TujuanDinas)
admin.site.register(StatusModel)
admin.site.register(KategoriBiaya)
admin.site.register(PengajuanDinas)
admin.site.register(BiayaPerjalanan)
