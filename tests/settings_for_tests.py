try:
    from foodgram.settings import *
except ImportError:
    raise AssertionError(
        "установите правильные пути импорта файла с настройками проекта "
        "`foodgram.settings` в файл `/tests/settings_for_tests.py:2`"
    )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
