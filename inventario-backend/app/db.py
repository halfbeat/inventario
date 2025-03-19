""" Módulo con las clases y objetos básicos de acceso a la base de datos"""

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.pagination import Pagination

db = SQLAlchemy()


class BaseModelMixin:
    """Clase base con los métodos básicos de las entidades de base de datos"""

    def save(self):
        """Persiste un DTO en la base de datos"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Elimina un DTO de la base de datos"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_paged(cls, page: int, page_size: int) -> Pagination:
        """
        Recupera todos los registros de forma paginada de una entidad
        :param page: Nº de página a mostrar
        :param page_size: Tamañp de la página
        :return: Objeto Pagination que representa la información paginada
        """
        if page < 1:
            raise IndexError("El nº de página no es válido")
        if page_size < 1:
            raise IndexError("El tamaño de página no es válido")
        return db.paginate(db.select(cls), page=page, per_page=page_size, error_out=False)

    @classmethod
    def count_all(cls):
        """Devuelve el nº de registros del DTO"""
        return db.count(db.select(cls))

    @classmethod
    def get_all(cls):
        """Devuelve todos los registros del DTO"""
        return db.session.execute(db.select(cls)).scalars()

    @classmethod
    def get_by_id(cls, **kwargs):
        return db.session.execute(db.select(cls).filter_by(**kwargs)).scalar_one()

    @classmethod
    def simple_filter(cls, **kwargs):
        return db.session.execute(db.select(cls).filter_by(**kwargs)).scalars()

    @classmethod
    def simple_count(cls, **kwargs):
        return db.count(db.select(cls).where(**kwargs))

    @classmethod
    def simple_page_filter(cls, page, page_size, **kwargs):
        if page < 1:
            raise IndexError("El nº de página no es válido")
        if page_size < 1:
            raise IndexError("El tamaño de página no es válido")
        return db.paginate(db.select(cls).filter_by(**kwargs), page=page, per_page=page_size, error_out=False)
