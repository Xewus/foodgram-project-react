from core.enums import Limits

"""help-texts for users.models"""
# help-text для email
USERS_HELP_EMAIL = (
    'Обязательно для заполнения. '
    f'Максимум {Limits.MAX_LEN_EMAIL_FIELD} букв.'
)
# help-text для username
USERS_HELP_UNAME = (
    'Обязательно для заполнения. '
    f'От {Limits.MIN_LEN_USERNAME} до {Limits.MAX_LEN_USERS_CHARFIELD} букв.'
)

# help-text для first_name/last_name
USERS_HELP_FNAME = (
    'Обязательно для заполнения. '
    f'Максимум {Limits.MAX_LEN_USERS_CHARFIELD} букв.'
)
