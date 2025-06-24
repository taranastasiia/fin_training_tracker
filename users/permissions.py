from training_tracker.permissions import CustomBasePermission
from training_tracker.permissions import DjangoViewAction


class UserPermission(CustomBasePermission):
    allowed_actions = [DjangoViewAction.RETRIEVE.value,
                       DjangoViewAction.UPDATE.value,
                       DjangoViewAction.PARTIAL_UPDATE.value,
                       DjangoViewAction.DELETE.value,
                       DjangoViewAction.LIST.value]