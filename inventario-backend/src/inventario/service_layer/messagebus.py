# pylint: disable=broad-except
from __future__ import annotations

import logging
from typing import List, Dict, Callable, Type, Union, TYPE_CHECKING

from . import handlers
from ..domain import commands, events

if TYPE_CHECKING:
    from . import unit_of_work, handlers

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


def handle(
        message: Message,
        uow: unit_of_work.AbstractUnitOfWork,
):
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, events.Event):
            handle_event(message, queue, uow)
        elif isinstance(message, commands.Command):
            cmd_result = handle_command(message, queue, uow)
            results.append(cmd_result)
        else:
            raise Exception(f"{message} was not an Event or Command")
    return results


def handle_event(
        event: events.Event,
        queue: List[Message],
        uow: unit_of_work.AbstractUnitOfWork,
):
    if EVENT_HANDLERS.get(type(event)) is None:
        return

    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug("handling event %s with handler %s", event, handler)
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling event %s", event)
            continue


def handle_command(
        command: commands.Command,
        queue: List[Message],
        uow: unit_of_work.AbstractUnitOfWork,
):
    logger.debug("handling command %s", command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logger.exception("Exception handling command %s", command)
        raise


EVENT_HANDLERS = {
    # events.OutOfStock: [handlers.send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.RegistrarSistema: handlers.registrar_sistema,
    commands.ObtenerSistema: handlers.obtener_sistema,
    commands.ModificarSistema: handlers.modificar_sistema,
    commands.ModificarComponente: handlers.modificar_componente,
}  # type: Dict[Type[commands.Command], Callable]
