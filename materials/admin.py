from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from materials.models import Attribute, AttributeOption, MaterialAttribute, Material, \
    Recycler, RecyclerQuality


admin.site.register(Attribute, MPTTModelAdmin)
admin.site.register(AttributeOption)
admin.site.register(Material)
admin.site.register(MaterialAttribute)
admin.site.register(Recycler)
admin.site.register(RecyclerQuality)
