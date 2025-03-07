from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action

from common.views.mixins import LCRUDViewSet
from organisations.permissions import IsColleagues
from organisations.backends import OwnedByOrganisation
from organisations.filters import EmployeeFilter
from organisations.serializers.api import employees as employees_s
from organisations.models.organisations import Employee


@extend_schema_view(   # Этот декоратор добавляет аннотации для Swagger
    list=extend_schema(summary='Список сотрудников организации', tags=['Организации : Сотрудники']),
    retrieve=extend_schema(summary='Деталка сотрудника организации', tags=['Организации : Сотрудники']),
    create=extend_schema(summary='Создать сотрудника организации', tags=['Организации : Сотрудники']),
    update=extend_schema(summary='Обновить сотрудника организации', tags=['Организации : Сотрудники']),
    partial_update=extend_schema(summary='Изменить сотрудника организации частично', tags=['Организации : Сотрудники']),
    destroy=extend_schema(summary=' Удалить сотрудника из организации', tags=['Организации : Сотрудники']),
    search=extend_schema(filters=True, summary='Список сотрудников организации Search', tags=['Словари']),
)
class EmployeeView(LCRUDViewSet):
    queryset = Employee.objects.all()  # Django queryset запрос к модели Employee
    serializer_class = employees_s.EmployeeListSerializer  # Django serializer для списка сотрудников

    permission_classes = [IsColleagues]  # Django permissions для сотрудников

    multi_serializer_class = {  # Кастомный словарь сериализаторов
        'list': employees_s.EmployeeListSerializer,
        'retrieve': employees_s.EmployeeRetrieveSerializer,
        'create': employees_s.EmployeeCreateSerializer,
        'update': employees_s.EmployeeUpdateSerializer,
        'partial_update': employees_s.EmployeeUpdateSerializer,
        'search': employees_s.EmployeeSearchSerializer,
        'destroy': employees_s.EmployeeDeleteSerializer,
    }

    lookup_url_kwarg = 'employee_id'  # Django Имя параметра в URL для получения сотрудника
    http_method_names = ('get', 'post', 'patch', 'delete',)  # Django Разрешенные HTTP методы

    filter_backends = (  # Django Фильтры для списка сотрудников
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        OwnedByOrganisation,  # кастомный фильтр
    )
    filterset_class = EmployeeFilter
    ordering = ('position', 'date_joined', 'id',)

    def get_queryset(self):  # Django Метод для получения queryset
        qs = Employee.objects.select_related(
            'user',
            'position',
        ).prefetch_related(
            'organisation',
        )
        return qs

    @action(methods=['GET'], detail=False, url_path='search')  # Действие для поиска
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):  # Метод для удаления сотрудника
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=dict())
        serializer.is_valid(raise_exception=True)
        return super().destroy(request, *args, **kwargs)
