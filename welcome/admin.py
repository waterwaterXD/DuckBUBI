from django.contrib import admin
from .models import  Account
#Register your models here.


class Account_UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Account._meta.fields]  # 顯示所有資料
    # list_display = []
    # exclude = []  # admin資料無法更改
    # list_filter = ()  # 過濾
    search_fields = ('position', 'company')  # 搜尋欄位
    ordering = ('-userID',)

    def get_queryset(self, request):
        return super().get_queryset(request)


admin.site.register(Account, Account_UserAdmin)



