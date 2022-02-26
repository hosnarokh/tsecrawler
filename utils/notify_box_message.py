import copy

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from pyapp_users.models import UserProfile, User

from pyapp_notifbox.models import Message
from socials.models import Follow
from utils.custom_functions import user_name_show

"""
action= {
        '1':follow,
        '2':Like,
        '3':Comment,
        '4':New Social,
        '5':New Recipe,
        '6':Change Status Social
        }
"""

DATA_STRUCTURE = {
    "user": None,
    "action": None,
    "recipe": None,
    "time": timezone.now()
}

FOLLOW_ACTION = 1
LIKE_ACTION = 2
COMMENT_ACTION = 3
NEW_SOCIAL_ACTION = 4
NEW_RECIPE_ACTION = 5
CHANGE_STATUS_SOCIAL_ACTION = 6


def follow_notify_box(from_user, to_user):
    avatar = UserProfile.objects.get(user_id=from_user.id).avatar
    data = copy.deepcopy(DATA_STRUCTURE)
    data["user"] = from_user.id
    data["action"] = FOLLOW_ACTION
    body = _("user '%s' start following you. ") % user_name_show(from_user)
    title = "Following"
    message_image = avatar if avatar else None
    users = list(User.objects.filter(id=to_user.id))
    creator = from_user
    Message.create_message(body, data, title, message_image, creator, users)


def like_notify_box(user, recipe):
    data = copy.deepcopy(DATA_STRUCTURE)
    data["user"] = user.id
    data["action"] = LIKE_ACTION
    data["recipe"] = recipe.id
    body = _("user '%s' liked your recipe.") % user_name_show(user)
    title = "Like"
    message_image = recipe.recipe_image
    users = list(User.objects.filter(id=recipe.user.id))
    creator = user
    Message.create_message(body, data, title, message_image, creator, users)


def comment_notify_box(user, recipe):
    data = copy.deepcopy(DATA_STRUCTURE)
    data["user"] = user.id
    data["action"] = COMMENT_ACTION
    data["recipe"] = recipe.id
    body = _("user ' %s ' commented on your recipe.") % user_name_show(user)
    title = "Comment"
    message_image = recipe.recipe_image
    users = list(User.objects.filter(id=recipe.user.id))
    creator = user
    Message.create_message(body, data, title, message_image, creator, users)


def add_social_notify_box(recipe):
    data = copy.deepcopy(DATA_STRUCTURE)
    data["user"] = recipe.user_id
    data["action"] = NEW_SOCIAL_ACTION
    data["recipe"] = recipe.id
    body = _("user '%s' add new recipe: ' %s '") % (user_name_show(recipe.user), recipe.title)
    follows = list(Follow.objects.filter(to_user_id=recipe.user.id).all().values_list('from_user_id', flat=True))
    users = list(User.objects.filter(id__in=follows).all())
    title = "New Social"
    message_image = recipe.recipe_image
    creator = recipe.user
    Message.create_message(body, data, title, message_image, creator, users)


def add_recipe_notify_box(recipe):
    data = copy.deepcopy(DATA_STRUCTURE)
    data["action"] = NEW_RECIPE_ACTION
    data["recipe"] = recipe.id
    body = _("chef '%s' add new recipe:' %s '") % (recipe.chef.name, recipe.title)
    title = "New Recipe"
    message_image = recipe.recipe_image
    Message.create_message(body, data, title, message_image)


def change_status_social_notify_box(recipe):
    data = copy.deepcopy(DATA_STRUCTURE)
    data["action"] = CHANGE_STATUS_SOCIAL_ACTION
    data["recipe"] = recipe.id
    data["time"]: timezone.now()
    body = _("recipe status change to '%s'. ") % recipe.get_status_display()
    title = "Change Status Social"
    message_image = recipe.recipe_image.url
    users = list(User.objects.filter(id=recipe.user.id))
    Message.create_message(body, data, title, message_image, users=users)
