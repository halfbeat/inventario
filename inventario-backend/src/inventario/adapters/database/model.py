from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Date, Text, PrimaryKeyConstraint, ForeignKeyConstraint, Integer, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql.functions import now

db = SQLAlchemy()
metadata = db.metadata

Base = db.Model


class AuditoriaMixinModelDto(object):
    # Campos de auditoría
    usuario_creacion = Column("C_USR_CREACION", String(10))
    fecha_creacion = Column(
        "F_CREACION", DateTime(timezone=True), server_default=now(), nullable=False
    )
    usuario_modificacion = Column("C_USR_MODIFICACION", String(10))
    fecha_modificacion = Column(
        "F_MODIFICACION", DateTime(timezone=True)
    )


class UnidadDir3ModelDto(Base):
    __tablename__ = "INVE_UNIDADES_DIR3"

    C_ID_UD_ORGANICA = Column("C_ID_UD_ORGANICA", String(9), nullable=False)
    C_DNM_UD_ORGANICA = Column("C_DNM_UD_ORGANICA", String(150), nullable=False)
    N_NIVEL_JERARQUICO = Column("N_NIVEL_JERARQUICO", Integer, nullable=True)
    C_ID_DEP_UD_SUPERIOR = Column("C_ID_DEP_UD_SUPERIOR", String(9), nullable=True)
    NIF_CIF = Column("NIF_CIF", String(9), nullable=True)
    C_DNM_UD_ORGANICA_SUPERIOR = Column("C_DNM_UD_ORGANICA_SUPERIOR", String(150), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint(C_ID_UD_ORGANICA),
        ForeignKeyConstraint(
            [C_ID_DEP_UD_SUPERIOR],
            [C_ID_UD_ORGANICA]
        )
    )


class PersoanaModelDto(Base, AuditoriaMixinModelDto):
    __tablename__ = "INVE_PERSONAS"
    persona_id = Column("C_PERSONA_ID", Integer, autoincrement=True)
    nombre = Column("D_NOMBRE", String(50), nullable=False)
    apellido1 = Column("D_APELLIDO1", String(50), nullable=False)
    apellido2 = Column("D_APELLIDO2", String(50), nullable=False)
    email = Column("D_EMAIL", String(50), nullable=False)
    ldap_id = Column("D_LDAP_ID", String(50), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint(persona_id),
        {}
    )


class SistemaInformacionModelDto(Base, AuditoriaMixinModelDto):
    __tablename__ = "INVE_SISTEMAS"
    sistema_id = Column("C_SISINFO_ID", String(10))
    nombre = Column("D_NOMBRE", String(50), nullable=False)
    unidad_responsable = Column("C_UNIDAD_FUNCIONAL_ID", String(9))
    tecnico_responsable = Column("C_RESPONSABLE_TECNICO_ID", Integer)
    fecha_entrada_produccion = Column(
        "F_PUESTA_PRODUCCION", Date(),
        nullable=True,
    )
    fecha_salida_produccion = Column(
        "F_SALIDA_PRODUCCION", Date(),
        nullable=True,
    )
    observaciones = Column(
        "D_OBSERVACIONES", Text(), nullable=True
    )
    componentes: Mapped[List["ComponenteModelDto"]] = relationship(back_populates="sistema")

    __table_args__ = (
        PrimaryKeyConstraint(sistema_id),
        ForeignKeyConstraint(
            [tecnico_responsable],
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
        self.unidad_responsable = kwargs.get("unidad_responsable", None)
        self.tecnico_responsable = kwargs.get("tecnico_responsable", None)
        self.observaciones = kwargs.get("observaciones", None)

class TipoComponenteModelDto(Base):
    __tablename__ = 'INVE_TIPOS_COMPONENTE'
    tipo_componente = Column("C_TP_COMPONENTE_ID", String(20), nullable=False)
    nombre = Column("D_NOMBRE", String(50), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(tipo_componente),
    )

class ComponenteModelDto(Base, AuditoriaMixinModelDto):
    __tablename__ = "INVE_COMPONENTES"
    sistema_id = Column("C_SISINFO_ID", String(10))
    componente_id = Column("C_COMPONENTE_ID", String(10))
    tipo = Column("C_TP_COMPONENTE_ID", String(20), nullable=False)
    componente_padre_id = Column("C_COMPONENTE_PADRE_ID", String(10))
    nombre = Column("D_NOMBRE", String(50), nullable=False)
    url_proyecto_git = Column("D_GIT_PROJECT", String(500), nullable=True)
    observaciones = Column(
        "D_OBSERVACIONES", Text(), nullable=True
    )
    sistema: Mapped[SistemaInformacionModelDto] = relationship(back_populates="componentes")

    __table_args__ = (
        PrimaryKeyConstraint(sistema_id, componente_id),
        ForeignKeyConstraint(
            [sistema_id],
            [SistemaInformacionModelDto.sistema_id]
        ),
        ForeignKeyConstraint(
            [tipo],
            [TipoComponenteModelDto.tipo_componente]
        ),
        ForeignKeyConstraint(
            [sistema_id, componente_padre_id],
            [sistema_id, componente_id]
        ),
    )

    def __init__(
            self,
            **kwargs
    ):
        self.sistema_id = kwargs.get("sistema_id")
        self.componente_id = kwargs.get("componente_id")
        self.tipo = kwargs.get("tipo")
        self.nombre = kwargs.get("nombre")
        self.componente_padre_id = kwargs.get("componente_padre_id", None)
        self.url_proyecto_git = kwargs.get("url_proyecto_git", None)
        self.observaciones = kwargs.get("observaciones", None)
