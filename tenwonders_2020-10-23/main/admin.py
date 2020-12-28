from django.contrib import admin
from .models import *
# Register your models here.
from import_export.admin import ImportExportModelAdmin


@admin.register(Influencer_DB,Youtube_result,Instagram_result,Search,Log,Work,ID_btn,Notice,Meeting)
class InfluencerAdmin(ImportExportModelAdmin):
    pass


