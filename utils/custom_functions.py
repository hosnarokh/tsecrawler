from pyapp_users.models import UserProfile


def user_name_show(user):
    user_profile = UserProfile.objects.filter(user=user).first()
    if user_profile and not user_profile.nick_name == '':
        return user_profile.nick_name
    return "user %s " % user.id


