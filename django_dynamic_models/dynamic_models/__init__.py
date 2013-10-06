import dynamic_models.models
from dynamic_models.models import DynamicModel
from dynamic_models.utils import text_description_to_model

try:
    for dm in DynamicModel.objects.filter(is_created=True):
        text_description_to_model(
            dynamic_models.models,
            dm.description,
            'dynamic_models',
            verbosity=True
        )
except Exception:
    pass