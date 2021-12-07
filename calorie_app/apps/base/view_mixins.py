from apps.users import constants as user_constants


class CurrentUserQuerySetMixin:

    def get_queryset(self):
        queryset = super().get_queryset()

        # To escape unnecessary swagger warnings
        if getattr(self, "swagger_fake_view", False):
            return queryset.none()

        if self.request.user.role == user_constants.UserRoles.ADMIN:
            return queryset
        return queryset.filter(user_id=self.request.user.user_id)


class MultiplePermissionMixin:
    def get_permissions(self):
        if not hasattr(self, 'permission_classes_map'):
            return super().get_permissions()

        permissions = self.permission_classes_map.get(
            self.action, self.permission_classes
        )
        return [permission() for permission in permissions]


class MultipleSerializerMixin:

    def get_serializer_class(self):
        # If serializer classes map is not present we return default serializer
        if not hasattr(self, 'serializer_classes'):
            return self.serializer_class

        return self.serializer_classes.get(self.action, self.serializer_class)
