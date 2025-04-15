from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain import commands

if TYPE_CHECKING:
    from . import unit_of_work

def obtener_sistema(
        cmd: commands.ObtenerSistema,
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        return uow.sistemas.get(cmd.sistema_id)


def buscar_unidades_dir3(
        cmd: commands.BuscarUnidadesDir3,
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        return []
