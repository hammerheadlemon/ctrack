from django.contrib import admin

from .models import Organisation, Address, AddressType


class OrganisationAdmin(admin.ModelAdmin):
    pass


class AddressTypeAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(AddressType, AddressTypeAdmin)
admin.site.register(Address, AddressAdmin)
