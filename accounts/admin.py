from django.contrib import admin

from . import models

# Register your models here.


admin.site.register(models.CustomUser)


@admin.register(models.RecycleUser)
class RecycleUserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return models.RecycleUser.delete_object.filter(is_deleted=True)
