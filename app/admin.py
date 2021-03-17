from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from app.models import Project, Task


class TaskAdmin(MPTTModelAdmin):
    mptt_level_indent = 30
    list_display = ('title', 'start', 'duration', 'employee_count', 'salary', 'parent', 'project')
    list_editable = ('start', 'duration', 'employee_count', 'salary', 'parent', 'project')
    list_filter = ('project',)


admin.site.register(Task, TaskAdmin)
admin.site.register(Project)
