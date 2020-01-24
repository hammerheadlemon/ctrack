from django.contrib import admin

from .models import Organisation, Address, AddressType


class AddressTypeAdmin(admin.ModelAdmin):
    pass


class AddressInLine(admin.StackedInline):
    model = Address
    max_num = 3
    extra = 1


class OrganisationAdmin(admin.ModelAdmin):
    inlines = [AddressInLine,]
    list_display = ('slug', 'name')


# Register your models here.
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(AddressType, AddressTypeAdmin)
