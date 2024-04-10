from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action


from common.views.mixins import CRUDViewSet, ListViewSet
from organisations.permissions import IsColleagues
from organisations.backends import OwnedByOrganisation
from organisations.filters import EmployeeFilter
from organisations.serializers.api import employees as employees_s
from organisations.models.organisations import Employee


@extend_schema_view(
    list=extend_schema(summary='Список сотрудников Search', tags=['Словари']),
)
class OrganisationSearchView(ListViewSet):
    queryset = Employee.objects.all()
    serializer_class = employees_s.EmployeeSearchSerializer

    filter_backends = (OwnedByOrganisation,)

    def get_queryset(self):
        qs = Employee.objects.select_related(
            'user',
            'position',
        ).prefetch_related(
            'organisation',
        )
        return qs



@extend_schema_view(
    list=extend_schema(summary='Список сотрудников организации', tags=['Организации : Сотрудники']),
    retrieve=extend_schema(summary='Деталка сотрудника организации', tags=['Организации : Сотрудники']),
    create=extend_schema(summary='Создать сотрудника организации', tags=['Организации : Сотрудники']),
    update=extend_schema(summary='Обновить сотрудника организации', tags=['Организации : Сотрудники']),
    partial_update=extend_schema(summary='Изменить сотрудника организации частично', tags=['Организации : Сотрудники']),
    destroy=extend_schema(summary=' Удалить сотрудника из организации', tags=['Организации : Сотрудники']),
    search=extend_schema(filters=True, summary='Список сотрудников организации Search', tags=['Словари']),
)
class EmployeeView(CRUDViewSet):
    queryset = Employee.objects.all()
    serializer_class = employees_s.EmployeeListSerializer

    permission_classes = [IsColleagues]

    multi_serializer_class = {
      'list': employees_s.EmployeeListSerializer,
      'retrieve': employees_s.EmployeeRetrieveSerializer,
      'create': employees_s.EmployeeCreateSerializer,
      'update': employees_s.EmployeeUpdateSerializer,
      'partial_update': employees_s.EmployeeUpdateSerializer,
      'search': employees_s.EmployeeSearchSerializer,
    #   'destroy': employees_s.EmployeeDeleteSerializer,
    }

    lookup_url_kwarg = 'employee_id'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        OwnedByOrganisation,
    )
    filterset_class = EmployeeFilter
    ordering = ('position', 'date_joined', 'id',)

    def get_queryset(self):
        qs = Employee.objects.select_related(
            'user',
            'position',
        ).prefetch_related(
            'organisation',
        )
        return qs
    
    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request, *args, **kwargs):
        return super().search(request, *args, **kwargs)
    
