from django.contrib import admin
from django.contrib.admin import TabularInline
from breaks.models import organisations, groups, replacement

########################################################
# INLINES
########################################################
class ReplacementEmployeeInline(TabularInline):
    model = replacement.ReplacementEmployee
    fields = ('employee', 'status',)




########################################################
# MODELS
########################################################

@admin.register(organisations.Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director'
    )

@admin.register(groups.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'min_active'
    )

@admin.register(replacement.ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'sort', 'is_active',
    )

@admin.register(replacement.Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'group', 'date', 'break_start', 'break_end', 'break_max_duration',
    )

    inlines = (
        ReplacementEmployeeInline,
    )




