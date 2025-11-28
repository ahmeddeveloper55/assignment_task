from django.apps import apps


def get_model(app_label, model_name):
    """
    Returns the Model with the given app_label and model_name. As a shortcut,
    this method also accepts a single argument in the form app_label.model_name.
    model_name is case-insensitive.
    """
    return apps.get_model(app_label=app_label, model_name=model_name)
