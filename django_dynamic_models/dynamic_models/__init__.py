from django.conf import settings

import models
from .utils import text_description_to_model


if not settings.TESTING:
    try:
        for dm in models.DynamicModel.objects.filter(is_created=True):
            text_description_to_model(
                models,
                dm.description,
                'dynamic_models',
                verbosity=True
            )
    except Exception:
        pass