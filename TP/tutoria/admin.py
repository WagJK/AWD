from django.contrib import admin
from .models import Course
import bulk_admin
# Register your models here.
class CourseAdmin(bulk_admin.BulkModelAdmin):
    list_display = ('university','code', 'description') # list
    search_fields = ('university','code')
    fieldsets = (
        ['Main',{
            'fields':('university','code'),
        }],
        ['Advance',{
            'classes': ('collapse',), # CSS
            'fields': ('description',),
        }]
    )
admin.site.register(Course,CourseAdmin)