from django.contrib import admin


class MyAdmin(admin.ModelAdmin):
    def log_addition(self, *args):
            return
    def log_change(self, *args):
            return
    def log_deletion(self, *args):
            return
