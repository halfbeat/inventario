from sqlalchemy import text

from .model import SistemaInformacionViewDto
from ...service_layer import unit_of_work


def sistema(sistema: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(text(
            """
            SELECT * FROM INVE_SISTEMAS WHERE C_SISINFO_ID = :sistema
            """),
            dict(sistema=sistema),
        )
    result = [r._asdict() for r in results].pop(0)
    if not result:
        return None

    return SistemaInformacionViewDto(
        sistema_id=result["C_SISINFO_ID"],
        nombre=result["D_NOMBRE"],
    )
