from sqlalchemy import text

from sqlalchemy import text

from .model import ListadoPaginadoResumenSistemasViewDto, ResumenSistemaInformacionViewDto
from ..database.model import SistemaInformacionModelDto
from ...service_layer import unit_of_work


def to_view(row):
    r = row._asdict()
    return ResumenSistemaInformacionViewDto(
        sistema_id=r["C_SISINFO_ID"],
        nombre=r["D_NOMBRE"]
    )


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

    return ListadoPaginadoResumenSistemasViewDto(
        items=[to_view(r) for r in results],
        total=count,
        page=page,
        page_size=page_size
    )
