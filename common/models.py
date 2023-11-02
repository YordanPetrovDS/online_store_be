from django.db import models
from django.utils import timezone


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

    class Meta:
        abstract = True
