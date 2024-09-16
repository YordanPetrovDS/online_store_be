import random
import string
from pathlib import Path


def add_prefix(filename: str, number_of_letters: int = 6) -> str:
    """Adds a random prefix to the filename."""
    prefix = "".join(random.choices(string.ascii_lowercase, k=number_of_letters))
    return f"{prefix}_{filename}"


def get_upload_path(instance, filename: str):
    """Returns a path for the file upload based on the app label, model name and filename with 6 digits prefix."""
    filename = add_prefix(filename)
    return Path(instance._meta.app_label, instance._meta.model_name, filename)


def delete_old_file(instance, field_name: str):
    """Deletes the old file from storage if it exists."""
    old_instance = instance.__class__.objects.get(pk=instance.pk)
    old_file = getattr(old_instance, field_name, None)
    if old_file and old_file != getattr(instance, field_name, None):
        old_file.delete(save=False)
