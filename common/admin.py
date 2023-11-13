class IsActiveColumnMixin:
    def is_active(self, obj):
        return not obj.deleted_at

    is_active.boolean = True
