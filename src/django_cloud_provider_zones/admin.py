from django.contrib import admin

from .models import CloudProvider, CloudRegion, CloudAvailabilityZone

class CloudRegionAdmin(admin.ModelAdmin):
    list_display = ["provider", "region_name", "region_name_short"]
    list_filter = ["provider",]
    search_fields = ["provider__provider", "region_name", "region_name_short"]
    show_facets = admin.ShowFacets.ALWAYS

admin.site.register(CloudProvider)
admin.site.register(CloudRegion)
admin.site.register(CloudAvailabilityZone)

