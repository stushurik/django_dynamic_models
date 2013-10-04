from django.db.models import Model, TextField, BooleanField


class DynamicModel(Model):
    description = TextField(null=False, blank=False)
    is_created = BooleanField(default=False)
