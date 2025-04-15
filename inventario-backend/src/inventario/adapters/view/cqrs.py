from sqlalchemy import text

from .model import ListadoPaginadoResumenSistemasViewDto, ResumenSistemaInformacionViewDto, \
    ListadoPaginadoEntidadDir3ViewDto, EntidadDir3ViewDto
from ..database.model import SistemaInformacionModelDto, UnidadDir3ModelDto
from ...service_layer import unit_of_work
from sqlalchemy import text

from .model import ListadoPaginadoResumenSistemasViewDto, ResumenSistemaInformacionViewDto, \
    ListadoPaginadoEntidadDir3ViewDto, EntidadDir3ViewDto
from ..database.model import SistemaInformacionModelDto, UnidadDir3ModelDto
from ...service_layer import unit_of_work


def sistemas(page: int, page_size: int, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(text(
            """
            SELECT * FROM INVE_SISTEMAS 
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


def unidades_dir3(id: str, nombre: str, page: int, page_size: int, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with (uow):
        results = uow.session.query(UnidadDir3ModelDto).filter_by(C_ID_UD_ORGANICA=id, C_DNM_UD_ORGANICA=nombre).limit(
            page_size).offset(page * page_size).all()

    count = uow.session.query(UnidadDir3ModelDto).count()

    def to_view(row):
        return EntidadDir3ViewDto(
            codigo_dir3=row["C_ID_UD_ORGANICA"],
            nombre=row["C_DNM_UD_ORGANICA"]
        )

    return ListadoPaginadoEntidadDir3ViewDto(
        items=[to_view(r) for r in results],
        total=count,
        page=page,
        page_size=page_size
    )
