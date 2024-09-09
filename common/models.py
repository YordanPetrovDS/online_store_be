from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.db import models
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone
from tinify import Source, tinify

from utils.functions import delete_old_file
from utils.logging import log_error


class ActiveObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class DeletedObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(deleted_at__isnull=True)


class BaseModel(models.Model):
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveObjectsManager()
    deleted_objects = DeletedObjectsManager()
    all_objects = models.Manager()

    def soft_delete(self):
        """We do not override delete() on purpose to allow hard deletion in admin panel"""
        self.deleted_at = timezone.now()
        self.save()

    def restore_from_soft_deleted(self):
        self.deleted_at = None
        self.save()

    def save(self, *args, **kwargs):
        if self.pk:
            for field in self._meta.fields:
                if isinstance(field, (models.FileField, models.ImageField)):
                    # Delete the old file from storage if it exists
                    try:
                        delete_old_file(self, field.name)
                    except Exception as e:
                        log_error(f"Error deleting old file: {e}")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class TinifiedImageFieldFile(ImageFieldFile):
    """Before saving the uploaded image, compress it using Tinify API"""

    def save(self, name, content, save=True):
        if settings.TINIFY_COMPRESSION_ENABLED:
            content = self.compress_image_with_tinify(name, content)
        super().save(name, content, save)

    @staticmethod
    def compress_image_with_tinify(name: str, content: UploadedFile) -> UploadedFile:
        """Replace uploaded image with compressed one"""
        try:
            tinify.key = settings.TINIFY_API_KEY
            source: Source = tinify.from_buffer(content.read())
            compressed_content = SimpleUploadedFile(name, source.to_buffer(), content.content_type)
            # We do not need the old uploaded file anymore
            content.close()
            return compressed_content
        except tinify.Error as e:
            log_error(e.message)
        return content


class TinifiedImageField(ImageField):
    attr_class = TinifiedImageFieldFile
