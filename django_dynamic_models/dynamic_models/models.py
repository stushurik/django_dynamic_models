from django.db.models import Model, TextField, BooleanField


class DynamicModel(Model):
    description = TextField(null=False, blank=False)
    is_created = BooleanField(default=False)


def get_values_from_model(model, amount=None):
    step = amount
    start = 0
    while model.objects.all().exists():
        yield model.objects.all()[start: step] \
            if amount else model.objects.all()
        start = step
        step += amount
