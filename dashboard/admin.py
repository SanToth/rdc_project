from django.contrib import admin
from django.db.models import Q
from .models import Alarm, AlarmType, Cell, Comment, HwType, Site, SiteController, TerritorialDivision, Zone


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ['get_type_name', 'get_site_name', 'get_site_controller', 'check_result', 'created_at']
    list_filter = ['check_result', 'site__territorial_division__user', 'site__site_controller']
    raw_id_fields = ['type', 'cell', 'site']
    search_fields = ['type__name', 'type__title' , 'site__name', 'site__site_controller__name'] 

    def get_site_name(self, obj):
        return obj.site.name 
    get_site_name.short_description = 'Site/Object'

    def get_type_name(self, obj):
        return obj.type.name 
    get_type_name.short_description = 'Alarm Name'

    def get_site_controller(self, obj):
        return obj.site.site_controller.name 
    get_site_controller.short_description = 'Site Controller'

    # site__site_controller__name
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            search_term = search_term.strip()
            extra_queries = (Q(site__name__icontains=search_term),)
            queryset |= self.model.objects.filter(*extra_queries)
        return queryset, use_distinct


@admin.register(AlarmType)
class AlarmTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'description']
    search_fields = ['name', 'title', 'description']


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ['name', 'site', 'get_site_controller']
    list_filter = ['site__site_controller', 'site__territorial_division__user', 'site__territorial_division__zone']
    search_fields = ['name', 'site', 'get_site_controller']
    raw_id_fields = ['site']

    def get_site_controller(self, obj):
        return obj.site.site_controller.name 
    get_site_controller.short_description = 'Site Controller'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['alarm', 'user', 'created', 'updated']
    raw_id_fields = ['user', 'alarm']
    search_fields = ['text', 'user', 'alarm']


@admin.register(HwType)
class HwTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'hw_type', 'oss', 'site_controller', 'territorial_division']
    list_filter = ['hw_type', 'site_controller', 'territorial_division']
    raw_id_fields = ['hw_type', 'site_controller', 'territorial_division']
    search_fields = ['name']


@admin.register(SiteController)
class SiteControllerAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(TerritorialDivision)
class TerritorialDivisionAdmin(admin.ModelAdmin):
    list_display = ['zone', 'user']
    list_filter = ['user']
    raw_id_fields = ['zone', 'user']
    search_fields = ['zone', 'user']


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    search_fields = ['name']
