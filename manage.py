import os
import sys


def main():
    """Run administrative tasks."""
    settings = "online_store_api.test_settings" if "test" in sys.argv else "online_store_api.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
