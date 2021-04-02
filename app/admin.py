from django import forms
from django.contrib import admin
from app.models import Project, Task

from datetime import datetime


class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def clean(self):
        parents = self.cleaned_data.get('parents')

        if not parents:
            return self.cleaned_data

        end_dates = [datetime.strptime(p.end_date, '%Y-%m-%d').date() for p in parents]
        end_dates.sort(reverse=True)
        last_date = end_dates[0]

        start = self.cleaned_data.get('start')
        if start < last_date:
            self.add_error('start', f'Дочерняя задача не может начинаться раньше конца всех родительских. Не раньше {last_date}')
        return self.cleaned_data


class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = ('title', 'start', 'duration', 'employee_count', 'salary', 'project')
    list_editable = ('start', 'duration', 'employee_count', 'salary', 'project')
    list_filter = ('project',)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)


admin.site.register(Task, TaskAdmin)
admin.site.register(Project)
