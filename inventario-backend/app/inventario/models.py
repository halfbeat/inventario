"""Modelado ORM de entidades de base de datos utilizando SQLAlchemy"""
import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Set, List

from sqlalchemy import Enum, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, relationship

from app.db import db, BaseModelMixin
from sqlalchemy.orm import mapper, relationship


@dataclass
class Auditoria:
    """Datos básicos de auditoria"""
    usuario_creacion: str
    fecha_creacion: datetime = datetime.now()
    usuario_modificacion: str | None = None
    fecha_modificacion: datetime | None = None


class AuditoriaMixinModelDto(object):
    # Campos de auditoría
    usuario_creacion = db.Column("C_USR_CREACION", db.String(10))
    fecha_creacion = db.Column(
        "F_CREACION", db.DateTime(timezone=True), server_default=db.func.now()
    )
    usuario_modificacion = db.Column("C_USR_MODIFICACION", db.String(10))
    fecha_modificacion = db.Column(
        "F_MODIFICACION", db.DateTime(timezone=True)
    )

    def __init__(self,
                 usuario_creacion=None,
                 fecha_creacion=datetime.now(),
                 usuario_modificacion=None,
                 fecha_modificacion=None):
        self.update_auditoria(usuario_creacion, fecha_creacion, usuario_modificacion, fecha_modificacion)

    def update_auditoria(self,
                         usuario_creacion=None,
                         fecha_creacion=datetime.now(),
                         usuario_modificacion=None,
                         fecha_modificacion=None):
        self.usuario_creacion = usuario_creacion
        self.fecha_creacion = fecha_creacion
        self.usuario_modificacion = usuario_modificacion
        self.fecha_modificacion = fecha_modificacion


class UnidadDir3ModelDto(BaseModelMixin, db.Model):
    __tablename__ = "INVESGSS_UNIDADES_DIR3"

    C_ID_UD_ORGANICA = db.Column("C_ID_UD_ORGANICA", db.String(9), nullable=False)
    C_DNM_UD_ORGANICA = db.Column("C_DNM_UD_ORGANICA", db.String(150), nullable=False)
    N_NIVEL_JERARQUICO = db.Column("N_NIVEL_JERARQUICO", db.Integer, nullable=True)
    C_ID_DEP_UD_SUPERIOR = db.Column("C_ID_DEP_UD_SUPERIOR", db.String(9), nullable=True)
    NIF_CIF = db.Column("NIF_CIF", db.String(9), nullable=True)
    C_DNM_UD_ORGANICA_SUPERIOR = db.Column("C_DNM_UD_ORGANICA_SUPERIOR", db.String(150), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint(C_ID_UD_ORGANICA),
        ForeignKeyConstraint(
            [C_ID_DEP_UD_SUPERIOR],
            [C_ID_UD_ORGANICA]
        )
    )

    @classmethod
    def query(cls, page, page_size, unidad_id=None, nombre=None):
        filter_query = db.select(cls).filter()
        if unidad_id is not None:
            filter_query = filter_query.filter(UnidadDir3ModelDto.C_ID_UD_ORGANICA.like(f"%{unidad_id}%"))
        if nombre is not None:
            filter_query = filter_query.filter(UnidadDir3ModelDto.C_DNM_UD_ORGANICA.like(f"%{nombre}%"))
        paged = db.paginate(filter_query, page=page, per_page=page_size, error_out=False)
        return paged


class EmpresaModelDto(db.Model, BaseModelMixin, AuditoriaMixinModelDto):
    __tablename__ = "INVESGSS_EMPRESAS"
    empresa_id = db.Column("C_EMPRESA_ID", db.Integer, autoincrement=True)
    nombre = db.Column("D_NOMBRE", db.String(50), nullable=False)
    cif = db.Column("C_CIF", db.String(10), nullable=True)
    email = db.Column("D_EMAIL", db.String(50), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(empresa_id),
        {}
    )


class PersoanaModelDto(db.Model, BaseModelMixin, AuditoriaMixinModelDto):
    __tablename__ = "INVESGSS_PERSONAS"
    persona_id = db.Column("C_PERSONA_ID", db.Integer, autoincrement=True)
    nombre = db.Column("D_NOMBRE", db.String(50), nullable=False)
    apellido1 = db.Column("D_APELLIDO1", db.String(50), nullable=False)
    apellido2 = db.Column("D_APELLIDO2", db.String(50), nullable=False)
    email = db.Column("D_EMAIL", db.String(50), nullable=False)
    ldap_id = db.Column("D_LDAP_ID", db.String(50), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint(persona_id),
        {}
    )


class SistemaInformacionModelDto(AuditoriaMixinModelDto, db.Model, BaseModelMixin):
    """DTO de base de datos correspondiente a una aplicación    """
    __tablename__ = "INVEGSS_SISTEMAS"
    sistema_id = db.Column("C_SISINFO_ID", db.String(10))
    nombre = db.Column("D_NOMBRE", db.String(50), nullable=False)
    responsable_tecnico = db.Column("C_RESPONSABLE_TECNICO_ID", db.Integer)
    unidad_responsable = db.Column("C_UNIDAD_FUNCIONAL_ID", db.String(9))
    fecha_entrada_produccion = db.Column(
        "F_PUESTA_PRODUCCION", db.Date(),
        nullable=True,
    )
    fecha_salida_produccion = db.Column(
        "F_SALIDA_PRODUCCION", db.Date(),
        nullable=True,
    )
    observaciones = db.Column(
        "D_OBSERVACIONES", db.Text(), nullable=True
    )
    componentes: Mapped[List["ComponenteModelDto"]] = relationship(back_populates="sistema")

    __table_args__ = (
        PrimaryKeyConstraint(sistema_id),
        ForeignKeyConstraint(
            [responsable_tecnico],
            [PersoanaModelDto.persona_id]
        ),
        ForeignKeyConstraint(
            [unidad_responsable],
            [UnidadDir3ModelDto.C_ID_UD_ORGANICA]
        )
    )

    def __init__(
            self,
            **kwargs
    ):
        self.sistema_id = kwargs.get("sistema_id")
        self.nombre = kwargs.get("nombre")
        self.observaciones = kwargs.get("observaciones")
        super(SistemaInformacionModelDto, self).__init__(kwargs.get('usuario_creacion'), kwargs.get('fecha_creacion'),
                                                         kwargs.get('usuario_modificacion'),
                                                         kwargs.get('fecha_modificacion'))

    def update(
            self,
            **kwargs
    ):
        self.sistema_id = kwargs.get("sistema_id")
        self.nombre = kwargs.get("nombre")
        self.observaciones = kwargs.get("observaciones")
        self.unidad_responsable = kwargs.get("unidad_responsable")
        super(SistemaInformacionModelDto, self).update_auditoria(kwargs.get('usuario_creacion'),
                                                                 kwargs.get('fecha_creacion'),
                                                                 kwargs.get('usuario_modificacion'),
                                                                 kwargs.get('fecha_modificacion'))

    def __repr__(self):
        return f"Aplicacion([{self.sistema_id}] {self.nombre})"

    def __str__(self):
        return f"{self.nombre}"

    @classmethod
    def query_sistemas(
            cls, page, page_size, nombre=None, limitar_a_aplicaciones: list = None
    ):
        if not limitar_a_aplicaciones:
            if nombre == None:
                return super().get_all_paged(page, page_size)
            else:
                return db.paginate(
                    db.select(cls).filter(
                        SistemaInformacionModelDto.nombre.like(f"%{nombre}%")
                    ), page=page, per_page=page_size, error_out=False
                )
        else:
            if nombre == None:
                return db.paginate(
                    db.select(cls).filter(
                        SistemaInformacionModelDto.sistema_id.in_(limitar_a_aplicaciones)
                    ), page=page, per_page=page_size, error_out=False
                )
            else:
                return db.paginate(
                    db.select(cls).filter(
                        SistemaInformacionModelDto.nombre.like(f"%{nombre}%"),
                        SistemaInformacionModelDto.sistema_id.in_(limitar_a_aplicaciones),
                    ), page=page, per_page=page_size, error_out=False
                )


class TipoComponenteModelDto(db.Model, BaseModelMixin):
    __tablename__ = 'INVESGSS_TIPO_COMPONENTES'
    tipo_componente = db.Column("C_TP_COMPONENTE_ID", db.String(20), nullable=False)
    nombre = db.Column("D_NOMBRE", db.String(50), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(tipo_componente),

    )


class TagComponenteModelDto(db.Model, BaseModelMixin):
    __tablename__ = 'INVESGSS_TAGS'
    tag = db.Column("C_TAG_ID", db.String(20), nullable=False)
    descripcion = db.Column("D_DESCRIPCION", db.String(50), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint(tag),
    )


class TagsComponente(db.Model, BaseModelMixin):
    __tablename__ = "INVESGSS_TAGS_COMPONENTE"
    sistema_id = db.Column("C_SISINFO_ID", db.String(10))
    componente_id = db.Column("C_COMPONENTE_ID", db.String(10))
    tag = db.Column("C_TAG_ID", db.String(20), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(sistema_id, componente_id, tag),
        ForeignKeyConstraint(
            [sistema_id, componente_id],
            ["INVESGSS_COMPONENTES.C_SISINFO_ID", "INVESGSS_COMPONENTES.C_COMPONENTE_ID"]
        ),
        ForeignKeyConstraint(
            [tag],
            [TagComponenteModelDto.tag]
        ),
    )


class ComponenteModelDto(db.Model, BaseModelMixin, AuditoriaMixinModelDto):
    __tablename__ = "INVESGSS_COMPONENTES"
    sistema_id = db.Column("C_SISINFO_ID", db.String(10))
    componente_id = db.Column("C_COMPONENTE_ID", db.String(10))
    tipo_componente = db.Column("C_TP_COMPONENTE_ID", db.String(20), nullable=False)
    componente_padre_id = db.Column("C_COMPONENTE_PADRE_ID", db.String(10))
    nombre = db.Column("D_NOMBRE", db.String(50), nullable=False)
    git_project = db.Column("D_GIT_PROJECT", db.String(500), nullable=True)
    observaciones = db.Column(
        "D_OBSERVACIONES", db.Text(), nullable=True
    )
    sistema: Mapped[SistemaInformacionModelDto] = relationship(back_populates="componentes")
    tags: Mapped[Set[TagComponenteModelDto]] = relationship(secondary=TagsComponente.__table__)

    __table_args__ = (
        PrimaryKeyConstraint(sistema_id, componente_id),
        ForeignKeyConstraint(
            [sistema_id],
            [SistemaInformacionModelDto.sistema_id]
        ),
        ForeignKeyConstraint(
            [sistema_id, componente_padre_id],
            [sistema_id, componente_id]
        ),
        ForeignKeyConstraint(
            [tipo_componente],
            [TipoComponenteModelDto.tipo_componente]
        ),
    )

    def __init__(
            self,
            sistema_id,
            componente_id,
            nombre,
            usuario_creacion=None,
            fecha_creacion=datetime.now(),
            usuario_modificacion=None,
            fecha_modificacion=None
    ):
        super().__init__()
        self.sistema_id = sistema_id
        self.componente_id = componente_id
        self.nombre = nombre
        super(ComponenteModelDto, self).__init__(usuario_creacion, fecha_creacion, usuario_modificacion,
                                                 fecha_modificacion)


class RolAsignacionEnum(enum.Enum):
    JEFE_DE_PROYECTO = 'JEFE_DE_PROYECTO'
    ANALISTA = 'ANALISTA'
    DESARROLLADOR = 'DESARROLLADOR'


class AsignacionEmpresaComponenteModelDto(db.Model, BaseModelMixin):
    __tablename__ = "INVESGSS_EMPRESAS_COMPONENTES"
    empresa_id = db.Column("C_EMPRESA_ID", db.Integer)
    sistema_id = db.Column("C_SISINFO_ID", db.String(10))
    componente_id = db.Column("C_COMPONENTE_ID", db.String(10))
    fecha_inicio = db.Column(
        "F_INICIO", db.Date(),
    )
    fecha_fin_asignacion = db.Column("F_FIN", db.Date(), nullable=True)
    rol = db.Column("C_ROL_ID", Enum(RolAsignacionEnum), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(empresa_id, sistema_id, componente_id, fecha_inicio),
        ForeignKeyConstraint(
            [empresa_id],
            [EmpresaModelDto.empresa_id]
        ),
        ForeignKeyConstraint(
            [sistema_id, componente_id],
            [ComponenteModelDto.sistema_id, ComponenteModelDto.componente_id]
        )
    )

