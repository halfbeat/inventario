from sqlalchemy import text

from .model import ListadoPaginadoResumenSistemasViewDto, ResumenSistemaInformacionViewDto, \
    ListadoPaginadoEntidadDir3ViewDto, EntidadDir3ViewDto
from ..database.model import SistemaInformacionModelDto, UnidadDir3ModelDto
from ...service_layer import unit_of_work


def sistemas(page: int, page_size: int, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(text(
            """
            SELECT * FROM "INVE_SISTEMAS" 
            LIMIT :num_rows OFFSET :offset
            """),
            dict(offset=(page - 1) * page_size, num_rows=page_size),
        )

        count = uow.session.query(SistemaInformacionModelDto).count()

    def to_view(row):
        r = row._asdict()
        return ResumenSistemaInformacionViewDto(
            sistema_id=r["C_SISINFO_ID"],
            nombre=r["D_NOMBRE"]
        )

    return ListadoPaginadoResumenSistemasViewDto(
        items=[to_view(r) for r in results],
        total=count,
        page=page,
        page_size=page_size
    )

def unidad_to_view(model_entity):
    return EntidadDir3ViewDto(
        unidad_id=model_entity.C_ID_UD_ORGANICA,
        nombre=model_entity.C_DNM_UD_ORGANICA,
        unidad_padre_id=model_entity.C_ID_DEP_UD_SUPERIOR,
        nombre_unidad_padre=model_entity.C_DNM_UD_ORGANICA_SUPERIOR
    )

def unidades_dir3(id: str, nombre: str, page: int, page_size: int, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        filter_query = uow.session.query(UnidadDir3ModelDto)
        if id is not None:
            filter_query = filter_query.filter(UnidadDir3ModelDto.C_ID_UD_ORGANICA.like(f"%{id}%"))
        if nombre is not None:
            filter_query = filter_query.filter(UnidadDir3ModelDto.C_DNM_UD_ORGANICA.like(f"%{nombre}%"))
        results = filter_query.limit(page_size).offset((page - 1) * page_size).all()

        count = filter_query.count()

        return ListadoPaginadoEntidadDir3ViewDto(
            items=[unidad_to_view(r) for r in results],
            total=count,
            page=page,
            page_size=page_size
        )

def unidad_dir3(unidad_id: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        unidad = uow.session.query(UnidadDir3ModelDto).get(unidad_id)
        if unidad is None:
            return None

        return unidad_to_view(unidad)