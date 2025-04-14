from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import mapper, relationship, registry

from ..domain import model

db = SQLAlchemy()
metadata = db.metadata
mapper_registry = registry(metadata=metadata)

sistemas = Table(
    "INVE_SISTEMAS",
    metadata,
    Column("C_SISTEMA_ID", String(30), primary_key=True),
    Column("D_NOMBRE", String(50), nullable=False),
    Column("C_UNIDAD_FUNCIONAL_ID", String(9)),
    Column("D_OBSERVACIONES", Text()),
)

componentes = Table(
    "INVE_COMPONENTES",
    metadata,
    Column("C_SISTEMA_ID", String(30), ForeignKey("INVE_SISTEMAS.C_SISTEMA_ID"), primary_key=True),
    Column("C_COMPONENTE_ID", String(30), primary_key=True),
    Column("D_NOMBRE", String(50), nullable=False),
    Column("D_URL_PROYECTO_GIT", String(255)),
    Column("D_OBSERVACIONES", Text()),
)

def start_mappers():
    mapper_registry.map_imperatively(
        model.Sistema,
        sistemas,
        properties={
            "componentes": relationship("model.Componente", back_populates="sistema")
        }
    )
    mapper_registry.map_imperatively(
        model.Componente,
        componentes,
        properties={
            "sistema": relationship("model.Sistema", back_populates="componentes")
        })
    print("FINISH")
