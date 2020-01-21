from django.contrib import admin

from .models import Organisation, Address, AddressType


class AddressTypeAdmin(admin.ModelAdmin):
    pass


class AddressInLine(admin.StackedInline):
    model = Address


class OrganisationAdmin(admin.ModelAdmin):
    inlines = [AddressInLine,]


# Register your models here.
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(AddressType, AddressTypeAdmin)
