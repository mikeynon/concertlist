from __future__ import unicode_literals

from django.contrib import admin
from genlist.models import Event, searchBandSugg
# Register your models here.


admin.site.register(searchBandSugg)
admin.site.register(Event)