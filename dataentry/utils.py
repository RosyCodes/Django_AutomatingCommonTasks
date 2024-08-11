from django.apps import apps

# extracts only the user-created models
# excludes default models like Users, etc


def get_all_custom_models():
    # lists the default models that we dont want to display in our Upload Form
    default_models = ['ContentType', 'Session',
                      'LogEntry', 'Group', 'Permission', 'User', 'Upload']

    custom_models = []
    for model in apps.get_models():
        # print(model.__name__)
        # checks if the model name is in the list of  default model or not
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
        # print(model)
    return custom_models
