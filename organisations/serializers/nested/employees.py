from common.serializers.mixins import ExtendedModelSerializer
from organisations.models.organisations import Employee
from organisations.serializers.nested.dicts import PositionShortSerializer
from users.serializers.nested.users import UserShortSerializer

class EmployeeShortSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()
    position = PositionShortSerializer()

    class Meta:
        model = Employee
        fields = (
            'id',
            'user',
            'position',
        )