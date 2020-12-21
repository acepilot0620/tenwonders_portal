from django.contrib import admin
from .models import *
# Register your models here.
from import_export.admin import ImportExportModelAdmin


@admin.register(Influencer_DB,Youtube_result,Instagram_result,Search,Record,Contract,ID_btn)
class InfluencerAdmin(ImportExportModelAdmin):
    pass


