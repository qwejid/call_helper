from django.contrib import admin
# from django.contrib.admin import TabularInline, StackedInline
from organisations.models import organisations, groups, dicts
from breaks.models.replacement import GroupInfo

########################################################
# INLINES
########################################################
class EmployeeInline(admin.TabularInline):
    model = organisations.Employee
    fields = ('user', 'position', 'date_joined',)

class MemberInline(admin.TabularInline):
    model = groups.Member
    fields = ('user', 'date_joined',)

class ProfileBreakInline(admin.StackedInline):
    model = GroupInfo
    fields = (
        'min_active',
        'break_start',
        'break_end',
        'break_max_duration',) 
    
    

    

########################################################
# MODELS
########################################################
@admin.register(dicts.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'sort', 'is_active',
    )

@admin.register(organisations.Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director')
    filter_horizontal = ('employees', )
    inlines = (EmployeeInline,)

@admin.register(groups.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'min_active',)
    list_display_links = ('id', 'name',)
    search_fields = ("name",)
    inlines = (MemberInline,
               ProfileBreakInline,)
    

