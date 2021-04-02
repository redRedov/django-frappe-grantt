import json

from django.db.models import Max, Min
from django.views import generic
from django.shortcuts import get_object_or_404

from app.models import Project, Task


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def processing(self, task):
        new_task = {
            'id': str(task.pk),
            'name': task.title,
            'start': task.start_date,
            'end': task.end_date,
            'employee_count': task.employee_count,
            'salary': task.salary,
            'progress': 100,
            'price': task.price,
            'duration': task.duration,
        }

        children_pks = [ch.pk for ch in task.children.all()]
        new_task['dependencies'] = ','.join([str(pk) for pk in children_pks])
        return new_task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_pk = self.request.GET.get('id')
        tasks = Task.objects.filter(project__id=project_pk)
        context['tasks'] = []
        context['projects'] = Project.objects.all()
        context['project_pk'] = ''
        if project_pk:
            context['project'] = get_object_or_404(Project, pk=project_pk)
            context['project_pk'] = int(project_pk)
            context['tasks'] = [self.processing(t) for t in tasks.filter(parents=None)]
            context['tasks'] += [self.processing(t) for t in tasks.exclude(parents=None)]
            context['tasks'] = json.dumps(context['tasks'])
        return context

