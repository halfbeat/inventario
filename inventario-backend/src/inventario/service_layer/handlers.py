from __future__ import annotations

from typing import TYPE_CHECKING

from ..adapters.database.mapper import SistemaInformaciomDomainModelMapper
from ..domain import commands
from ..domain.model import Sistema

if TYPE_CHECKING:
    from . import unit_of_work


class SistemaNoEncontrado(Exception):
    pass


class SistemaExistente(Exception):
    pass


sistema_domain_model_mapper = SistemaInformaciomDomainModelMapper()


def obtener_sistema(
        cmd: commands.ObtenerSistema,
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        return uow.sistemas.get(cmd.sistema_id)


def registrar_sistema(
        cmd: commands.RegistrarSistema,
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        sistema = uow.sistemas.get(cmd.sistema_id)
        if sistema:
            raise SistemaExistente(f"El sistema {cmd.sistema_id} ya existe")

        sistema = Sistema(cmd.sistema_id, cmd.nombre, cmd.unidad_responsable, cmd.tecnico_responsable,
                          cmd.observaciones)

        uow.sistemas.update(sistema)
        uow.commit()

        return sistema


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


def modificar_componente(
        cmd: commands.ModificarComponente,
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        sistema = uow.sistemas.get(cmd.sistema_id)
        if not sistema:
            raise SistemaNoEncontrado()

        componente = next(
            iter([componente for componente in sistema.componentes if componente.componente_id == cmd.componente_id]),
            None)
        if not componente:
            componente = sistema.agregar_componente(cmd.componente_id, cmd.nombre, cmd.tipo, cmd.url_proyecto_git,
                                                    cmd.observaciones)
        else:
            componente.modificar(cmd.nombre, cmd.tipo, cmd.url_proyecto_git, cmd.observaciones)

        uow.sistemas.update(sistema)
        uow.commit()

        return componente
