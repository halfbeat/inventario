from __future__ import annotations

from typing import TYPE_CHECKING

from ..adapters.database.mapper import SistemaInformaciomDomainModelMapper
from ..domain import commands

if TYPE_CHECKING:
    from . import unit_of_work


class SistemaNoEncontrado(Exception):
    pass


sistema_domain_model_mapper = SistemaInformaciomDomainModelMapper()


def obtener_sistema(
        cmd: commands.ObtenerSistema,
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        return uow.sistemas.get(cmd.sistema_id)


def modificar_sistema(
        cmd: commands.ModificarSistema,
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        sistema = uow.sistemas.get(cmd.sistema_id)
        if not sistema:
            raise SistemaNoEncontrado()

        sistema.modificar(cmd.nombre, cmd.unidad_responsable, cmd.tecnico_responsable, cmd.observaciones)

        uow.sistemas.update(sistema)
        uow.commit()

        return sistema
