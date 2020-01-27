from django.contrib import admin

from .models import CAF, CAFFileStore, DocumentFile, Ranking

# Register your models here.

admin.site.register(CAF)
admin.site.register(CAFFileStore)
admin.site.register(DocumentFile)
admin.site.register(Ranking)
