from datetime import timedelta

from django.db import models
from django.db.models import F, Func, Sum
from django.db.models import DurationField, ExpressionWrapper, F
from mptt.models import MPTTModel, TreeForeignKey


class Project(models.Model):
    title = models.CharField('Название', max_length=200)
    author = models.CharField('Автор', max_length=200)
    day_hours = models.PositiveIntegerField('Количество рабочих часов в день', default=8, blank=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title

    @property
    def total_price(self):
        return self.tasks.aggregate(total=Sum(F('employee_count') * F('salary')))['total']

    @property
    def total_time(self):
        hours = self.tasks.aggregate(hours=Sum('duration'))['hours']
        return {
            'hours': self.tasks.aggregate(hours=Sum('duration'))['hours'],
            'days': round(hours / self.day_hours)
        }

    @property
    def start_date_project(self):
        return self.tasks.order_by('start').first().start

    @property
    def end_date_project(self):
        dates = [task.end_date for task in self.tasks.all()]
        dates.sort()
        return dates[-1] if dates else ''


class Task(MPTTModel):
    title = models.CharField('Название', max_length=200)
    start = models.DateField('Старт')
    duration = models.PositiveIntegerField('Количество часов')
    employee_count = models.PositiveIntegerField('Количество работников')
    salary = models.PositiveIntegerField('Ставка')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект', related_name='tasks')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

    @property
    def start_date(self):
        return self.start.strftime('%Y-%m-%d')

    @property
    def end_date(self):
        days = round(self.duration / self.project.day_hours)
        return (self.start + timedelta(days=days)).strftime('%Y-%m-%d')

    @property
    def price(self):
        return self.employee_count * self.salary
