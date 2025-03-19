"""Modelado ORM de entidades de base de datos utilizando SQLAlchemy"""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import ForeignKey, ForeignKeyConstraint, func, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from app.db import db, BaseModelMixin


@dataclass
class Auditoria:
    """Datos básicos de auditoria"""
    usuario_creacion: str
    fecha_creacion: datetime = datetime.now()
    usuario_modificacion: str | None = None
    fecha_modificacion: datetime | None = None


class AplicacionModelDto(db.Model, BaseModelMixin):
    """DTO de base de datos correspondiente a una aplicación    """
    __tablename__ = "AUTHZ_APLICACIONES"
    aplicacion_id = db.Column("C_APLICACION_ID", db.String(10), primary_key=True)
    nombre = db.Column("D_NOMBRE", db.String(50), nullable=False)

    # Campos de auditoría
    usuario_creacion = db.Column("C_USR_CREACION", db.String(10))
    fecha_creacion = db.Column(
        "F_CREACION", db.DateTime(timezone=True), server_default=db.func.now()
    )
    usuario_modificacion = db.Column("C_USR_MODIFICACION", db.String(10))
    fecha_modificacion: datetime = db.Column(
        "F_MODIFICACION", db.DateTime(timezone=True)
    )

    def __init__(
            self,
            aplicacion_id,
            nombre,
            usuario_creacion=None,
            fecha_creacion=datetime.now(),
            usuario_modificacion=None,
            fecha_modificacion=None,
    ):
        """Constructor de la clase

        aplicacion_id: str
            Identificador de la aplicación
        nombre: str
            Nombre de la aplicación
        usuario_creacion: str
            Principal del usuario que crea el registro
        fecha_creacion: datetime
            Fecha y hora de creación del registro
        usuario_modificacion: str | None
            Último usuario que actualiza el registro. None si el registro no se ha modificado
        fecha_modificacion: datetime | None
            Última fecha de modificación del registro. None si el registro no se ha modificado
        """
        self.aplicacion_id = aplicacion_id
        self.nombre = nombre
        self.usuario_creacion = usuario_creacion
        self.fecha_creacion = fecha_creacion
        self.usuario_modificacion = usuario_modificacion
        self.fecha_modificacion = fecha_modificacion

    def __repr__(self):
        return f"Aplicacion([{self.aplicacion_id}] {self.nombre})"

    def __str__(self):
        return f"{self.nombre}"

    @classmethod
    def query_aplicaciones(
            cls, page, page_size, nombre_app=None, limitar_a_aplicaciones: list = None
    ):
        if not limitar_a_aplicaciones:
            if nombre_app == None:
                return super().get_all_paged(page, page_size)
            else:
                return db.paginate(
                    db.select(cls).filter(
                        AplicacionModelDto.nombre.like(f"%{nombre_app}%")
                    ), page=page, per_page=page_size, error_out=False
                )
        else:
            if nombre_app == None:
                return db.paginate(
                    db.select(cls).filter(
                        AplicacionModelDto.aplicacion_id.in_(limitar_a_aplicaciones)
                    ), page=page, per_page=page_size, error_out=False
                )
            else:
                return db.paginate(
                    db.select(cls).filter(
                        AplicacionModelDto.nombre.like(f"%{nombre_app}%"),
                        AplicacionModelDto.aplicacion_id.in_(limitar_a_aplicaciones),
                    ), page=page, per_page=page_size, error_out=False
                )


class RolModelDto(db.Model, BaseModelMixin):
    __tablename__ = "AUTHZ_ROLES"
    aplicacion_id = db.Column(
        "C_APLICACION_ID",
        db.String(10),
        ForeignKey("AUTHZ_APLICACIONES.C_APLICACION_ID"),
        primary_key=True,
    )
    rol_id = db.Column("C_ROL_ID", db.String(10), primary_key=True)
    nombre = db.Column("D_NOMBRE", db.String(50), nullable=False)

    # Campos de auditoría
    usuario_creacion = db.Column("C_USR_CREACION", db.String(10))
    fecha_creacion = db.Column(
        "F_CREACION", db.DateTime(timezone=True), server_default=db.func.now()
    )
    usuario_modificacion = db.Column("C_USR_MODIFICACION", db.String(10))
    fecha_modificacion: datetime = db.Column(
        "F_MODIFICACION", db.DateTime(timezone=True)
    )

    def __init__(
            self,
            aplicacion_id,
            rol_id,
            nombre,
            usuario_creacion=None,
            fecha_creacion=datetime.now(),
            usuario_modificacion=None,
            fecha_modificacion=None,
    ):
        self.aplicacion_id = aplicacion_id
        self.rol_id = rol_id
        self.nombre = nombre
        self.usuario_creacion = usuario_creacion
        self.fecha_creacion = fecha_creacion
        self.usuario_modificacion = usuario_modificacion
        self.fecha_modificacion = fecha_modificacion


class PermisoModelDto(db.Model, BaseModelMixin):
    __tablename__ = "AUTHZ_PERMISOS"
    aplicacion_id = db.Column(
        "C_APLICACION_ID",
        db.String(10),
        ForeignKey("AUTHZ_APLICACIONES.C_APLICACION_ID"),
        primary_key=True,
    )
    permiso_id = db.Column("C_PERMISO_ID", db.String(50), primary_key=True)
    nombre = db.Column("D_NOMBRE", db.String(50), nullable=False)

    # Campos de auditoría
    usuario_creacion = db.Column("C_USR_CREACION", db.String(10))
    fecha_creacion = db.Column(
        "F_CREACION", db.DateTime(timezone=True), server_default=db.func.now()
    )
    usuario_modificacion = db.Column("C_USR_MODIFICACION", db.String(10))
    fecha_modificacion: datetime = db.Column(
        "F_MODIFICACION", db.DateTime(timezone=True)
    )

    def __init__(
            self,
            aplicacion_id,
            permiso_id,
            nombre,
            usuario_creacion=None,
            fecha_creacion=datetime.now(),
            usuario_modificacion=None,
            fecha_modificacion=None,
    ):
        self.aplicacion_id = aplicacion_id
        self.permiso_id = permiso_id
        self.nombre = nombre
        self.usuario_creacion = usuario_creacion
        self.fecha_creacion = fecha_creacion
        self.usuario_modificacion = usuario_modificacion
        self.fecha_modificacion = fecha_modificacion


class PermisosRolModelDto(db.Model, BaseModelMixin):
    __tablename__ = "AUTHZ_ROLES_PERMISOS"
    aplicacion_id = db.Column("C_APLICACION_ID", db.String(10), primary_key=True)
    rol_id = db.Column("C_ROL_ID", db.String(10), primary_key=True)
    permiso_id = db.Column("C_PERMISO_ID", db.String(50), primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            [aplicacion_id, rol_id], [RolModelDto.aplicacion_id, RolModelDto.rol_id]
        ),
        ForeignKeyConstraint(
            [aplicacion_id, permiso_id],
            [PermisoModelDto.aplicacion_id, PermisoModelDto.permiso_id],
        ),
        {},
    )

    permiso: Mapped["PermisoModelDto"] = relationship(viewonly=True)
    rol: Mapped["RolModelDto"] = relationship(viewonly=True)


class TipoAmbitoModelDto(db.Model, BaseModelMixin):
    __tablename__ = "AUTHZ_TIPOS_AMBITOS"
    tipo_ambito_id = db.Column("C_TP_AMBITO_ID", db.String(10), primary_key=True)
    tipo_ambito = db.Column("D_TP_AMBITO", db.String(50), nullable=False)
    restriccion = db.Column("D_RESTRICCION", db.String(100))


class AsignacionRolModelDto(db.Model, BaseModelMixin):
    __tablename__ = "AUTHZ_ASGN_ROLES"
    principal = db.Column("C_PRINCIPAL_ID", db.String(100))
    aplicacion_id = db.Column("C_APLICACION_ID", db.String(10))
    rol_id = db.Column("C_ROL_ID", db.String(10))
    n_orden = db.Column("N_ORDEN", db.Numeric(3))
    tipo_ambito = db.Column("C_TP_AMBITO_ID", db.String(10))
    ambito = db.Column("D_AMBITO", db.String(40))
    fecha_inicio = db.Column("F_INICIO", db.DateTime(timezone=True))
    fecha_fin = db.Column("F_FIN", db.DateTime(timezone=True))

    __table_args__ = (
        PrimaryKeyConstraint(principal, aplicacion_id, rol_id, n_orden),
        ForeignKeyConstraint(
            [aplicacion_id, rol_id], [RolModelDto.aplicacion_id, RolModelDto.rol_id]
        ),
        ForeignKeyConstraint([tipo_ambito], [TipoAmbitoModelDto.tipo_ambito_id]),
        {},
    )

    @staticmethod
    def filter(aplicacion: str, principal: str):
        return db.session.execute(db.select(AsignacionRolModelDto).filter(
            func.lower(AsignacionRolModelDto.principal) == func.lower(principal),
            AsignacionRolModelDto.aplicacion_id == aplicacion)).scalars()


class AsignacionPermisoModelDto(db.Model, BaseModelMixin):
    __tablename__ = "AUTHZ_ASGN_PERMISOS"
    principal = db.Column("C_PRINCIPAL_ID", db.String(100))
    aplicacion_id = db.Column("C_APLICACION_ID", db.String(10))
    permiso_id = db.Column("C_PERMISO_ID", db.String(50))
    n_orden = db.Column("N_ORDEN", db.Numeric(3))
    tipo_ambito = db.Column("C_TP_AMBITO_ID", db.String(10))
    ambito = db.Column("D_AMBITO", db.String(40))

    __table_args__ = (
        PrimaryKeyConstraint(principal, aplicacion_id, permiso_id, n_orden),
        ForeignKeyConstraint(
            [aplicacion_id, permiso_id],
            [PermisoModelDto.aplicacion_id, PermisoModelDto.permiso_id],
        ),
        ForeignKeyConstraint([tipo_ambito], [TipoAmbitoModelDto.tipo_ambito_id]),
        {},
    )
