from django.contrib import admin
from .models import Choose, Comment


class ChooseAdmin(admin.ModelAdmin):
    list_display = ("count_black", "count_white", "count_purple", "voter")
    list_display_links = ("count_black", "count_white", "count_purple", "voter")
    search_fields = ("count_black", "count_white", "count_purple", "voter")


admin.site.register(Choose, ChooseAdmin)
admin.site.register(Comment)
