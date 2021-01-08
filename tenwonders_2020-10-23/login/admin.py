from django.contrib import admin
from .models import Account
# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['pk','user','nickname','nickname_length','position']
    list_display_links = ['nickname']
    search_fields = ['nickname']
    list_filter = ['position']
    def nickname_length(self, account):
        return f"{len(account.nickname)} 글자"
