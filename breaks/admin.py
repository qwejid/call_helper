from django.contrib import admin
from django.contrib.admin import TabularInline
from django.urls import reverse
from breaks.models import dicts, breaks, replacements
from django.utils.html import format_html

########################################################
# INLINES
########################################################
class ReplacementMemberInline(TabularInline):
    model = replacements.ReplacementMember
    fields = ('member', 'status',)


########################################################
# MODELS
########################################################

@admin.register(dicts.ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'sort', 'is_active',
    )

@admin.register(dicts.BreakStatus)
class BreakStatusAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'sort', 'is_active',
    )

@admin.register(replacements.Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'group', 'date', 'break_start', 'break_end', 'break_max_duration',
    )
    # autocomplete_fields = ('group',)
    inlines = (
        ReplacementMemberInline,
    )

@admin.register(breaks.Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'replacement_link', 'break_start', 'break_end', "status",
    )
    list_filter = ('status',)
    empty_value_display = 'Unknown'
    radio_fields = {'status' : admin.VERTICAL}
    def replacement_link(self, obj):
        link = reverse(
            'admin:breaks_replacement_change', args=[obj.replacement.id]
        )
        return format_html('<a href="{}">{}</a>', link, obj.replacement)




