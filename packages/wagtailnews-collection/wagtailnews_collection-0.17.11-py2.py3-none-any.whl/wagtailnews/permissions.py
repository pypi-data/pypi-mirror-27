from .models import NEWSINDEX_MODEL_CLASSES


def format_perm(model, action):
    """
    Format a permission string "app.verb_model" for the model and the
    requested action (add, change, delete).
    """
    return '{meta.app_label}.{action}_{meta.model_name}'.format(
        meta=model._meta, action=action)


def format_perms(model, actions):
    """
    Make a list of permission strings "app.verb_model" for the model and the
    requested actions (add, change, delete).
    """
    return [format_perm(model, action) for action in actions]


def user_can_edit_news(user):
    """
    Check if the user has permission to edit any of the registered NewsItem
    types.
    """
    newsitem_models = [model.get_newsitem_model()
                       for model in NEWSINDEX_MODEL_CLASSES]

    if user.is_active and user.is_superuser:
        # admin can edit news iff any news types exist
        return bool(newsitem_models)

    return any(user.has_perm(perm)
        for NewsItem in newsitem_models
            for perm in format_perms(NewsItem, ['add', 'change', 'delete']))


def user_can_edit_newsitem(user, NewsItem):
    """
    Check if the user has permission to edit a particular NewsItem type.
    """
    return any(user.has_perm(perm)
        for perm in format_perms(NewsItem, ['add', 'change', 'delete']))

def perms_for_template(request, NewsItem):
    return {action: request.user.has_perm(format_perm(NewsItem, action))
            for action in ['add', 'change', 'delete']}
