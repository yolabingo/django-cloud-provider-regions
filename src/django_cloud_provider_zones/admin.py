from django.contrib import admin

from .models import CloudProvider, CloudRegion, CloudAvailabilityZone


class CloudRegionAdmin(admin.ModelAdmin):
    list_filter = ["provider"]
    list_display = ["region_name", "provider", "region_short_name"]
    search_fields = ["provider__provider", "region_name", "region_short_name"]


class CloudAvailabilityZoneAdmin(admin.ModelAdmin):
    list_filter = ["region"]
    list_display = ["az_name", "provider", "region", "az_short_name"]
    search_fields = [
        "provider__provider",
        "region__region_name",
        "az_name",
        "az_short_name",
    ]


admin.site.register(CloudProvider)
admin.site.register(CloudRegion, CloudRegionAdmin)
admin.site.register(CloudAvailabilityZone, CloudAvailabilityZoneAdmin)
