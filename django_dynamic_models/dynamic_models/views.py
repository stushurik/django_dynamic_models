# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response


def index_view(request):
    models = []
    for ct in ContentType.objects.all():
        instances = ct.model_class().objects.all()

        models.append({'model': ct.model,
                       'instances': instances
                       })
        print models
    return render_to_response('../templates/table.html', {'models': models})
