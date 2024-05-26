from common.views.mixins import DictListMixin
from breaks.models.dicts import ReplacementStatus
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(summary='Список статусов смен', tags=['Словари'])
)
class ReplacementStatusView(DictListMixin):
    model = ReplacementStatus
