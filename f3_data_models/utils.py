import os
from dataclasses import dataclass
from typing import List, Optional, Tuple, TypeVar

import sqlalchemy
from sqlalchemy import Select, and_, select

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, joinedload

from f3_data_models.models import Base

from pydot import Dot
from sqlalchemy_schemadisplay import create_schema_graph
from google.cloud.sql.connector import Connector, IPTypes
import pg8000


@dataclass
class DatabaseField:
    name: str
    value: object = None


GLOBAL_ENGINE = None
GLOBAL_SESSION = None


def get_engine(echo=False) -> Engine:
    host = os.environ["DATABASE_HOST"]
    user = os.environ["DATABASE_USER"]
    passwd = os.environ["DATABASE_PASSWORD"]
    database = os.environ["DATABASE_SCHEMA"]

    if os.environ.get("USE_GCP", "False") == "False":
        db_url = f"postgresql://{user}:{passwd}@{host}:5432/{database}"
        engine = sqlalchemy.create_engine(db_url, echo=echo)
    else:
        connector = Connector()

        def get_connection():
            conn: pg8000.dbapi.Connection = connector.connect(
                instance_connection_string=host,
                driver="pg8000",
                user=user,
                password=passwd,
                db=database,
                ip_type=IPTypes.PUBLIC,
            )
            return conn

        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://", creator=get_connection, echo=echo
        )
    return engine


def get_session(echo=True):
    if GLOBAL_SESSION:
        return GLOBAL_SESSION

    global GLOBAL_ENGINE
    GLOBAL_ENGINE = get_engine(echo=echo)
    return sessionmaker()(bind=GLOBAL_ENGINE)


def close_session(session):
    global GLOBAL_SESSION, GLOBAL_ENGINE
    if GLOBAL_SESSION == session:
        if GLOBAL_ENGINE:
            GLOBAL_ENGINE.close()
            GLOBAL_SESSION = None


T = TypeVar("T")


def _joinedloads(cls: T, query: Select, joinedloads: list | str) -> Select:
    if joinedloads == "all":
        joinedloads = [
            getattr(cls, relationship.key)
            for relationship in cls.__mapper__.relationships
        ]
    return query.options(*[joinedload(load) for load in joinedloads])


class DbManager:
    def get(cls: T, id: int, joinedloads: list | str = []) -> T:
        session = get_session()
        try:
            query = select(cls).filter(cls.id == id)
            query = _joinedloads(cls, query, joinedloads)
            return session.scalars(query).unique().one()
        finally:
            session.rollback()
            close_session(session)

    def find_records(
        cls: T, filters: Optional[List], joinedloads: List | str = []
    ) -> List[T]:
        session = get_session()
        try:
            query = select(cls)
            query = _joinedloads(cls, query, joinedloads)
            query = query.filter(*filters)
            records = session.scalars(query).unique().all()
            for r in records:
                session.expunge(r)
            return records
        finally:
            session.rollback()
            close_session(session)

    def find_first_record(
        cls: T, filters: Optional[List], joinedloads: List | str = []
    ) -> T:
        session = get_session()
        try:
            query = select(cls)
            query = _joinedloads(cls, query, joinedloads)
            query = query.filter(*filters)
            record = session.scalars(query).unique().first()
            if record:
                session.expunge(record)
            return record
        finally:
            session.rollback()
            close_session(session)

    def find_join_records2(left_cls: T, right_cls: T, filters) -> List[Tuple[T]]:
        session = get_session()
        try:
            records = (
                session.query(left_cls, right_cls)
                .join(right_cls)
                .filter(and_(*filters))
                .all()
            )
            session.expunge_all()
            return records
        finally:
            session.rollback()
            close_session(session)

    def find_join_records3(
        left_cls: T, right_cls1: T, right_cls2: T, filters, left_join=False
    ) -> List[Tuple[T]]:
        session = get_session()
        try:
            records = (
                session.query(left_cls, right_cls1, right_cls2)
                .select_from(left_cls)
                .join(right_cls1, isouter=left_join)
                .join(right_cls2, isouter=left_join)
                .filter(and_(*filters))
                .all()
            )
            session.expunge_all()
            return records
        finally:
            session.rollback()
            close_session(session)

    def update_record(cls: T, id, fields):
        session = get_session()
        try:
            session.query(cls).filter(cls.get_id() == id).update(
                fields, synchronize_session="fetch"
            )
            session.flush()
        finally:
            session.commit()
            close_session(session)

    def update_records(cls: T, filters, fields):
        session = get_session()
        try:
            session.query(cls).filter(and_(*filters)).update(
                fields, synchronize_session="fetch"
            )
            session.flush()
        finally:
            session.commit()
            close_session(session)

    def create_record(record: Base) -> Base:
        session = get_session()
        try:
            session.add(record)
            session.flush()
            session.expunge(record)
        finally:
            session.commit()
            close_session(session)
            return record  # noqa

    def create_records(records: List[Base]):
        session = get_session()
        try:
            session.add_all(records)
            session.flush()
            session.expunge_all()
        finally:
            session.commit()
            close_session(session)
            return records  # noqa

    def create_or_ignore(cls: T, records: List[Base]):
        session = get_session()
        try:
            for record in records:
                record_dict = {
                    k: v
                    for k, v in record.__dict__.items()
                    if k != "_sa_instance_state"
                }
                stmt = insert(cls).values(record_dict).on_conflict_do_nothing()
                session.execute(stmt)
            session.flush()
        finally:
            session.commit()
            close_session(session)

    def upsert_records(cls, records):
        session = get_session()
        try:
            for record in records:
                record_dict = {
                    k: v
                    for k, v in record.__dict__.items()
                    if k != "_sa_instance_state"
                }
                stmt = insert(cls).values(record_dict)
                update_dict = {
                    c.name: getattr(record, c.name) for c in cls.__table__.columns
                }
                stmt = stmt.on_conflict_do_update(
                    index_elements=[cls.__table__.primary_key.columns.keys()],
                    set_=update_dict,
                )
                session.execute(stmt)
            session.flush()
        finally:
            session.commit()
            close_session(session)

    def delete_record(cls: T, id):
        session = get_session()
        try:
            session.query(cls).filter(cls.get_id() == id).delete()
            session.flush()
        finally:
            session.commit()
            close_session(session)

    def delete_records(cls: T, filters, joinedloads: List | str = []):
        session = get_session()
        try:
            query = select(cls)
            query = _joinedloads(cls, query, joinedloads)
            query = query.filter(*filters)
            records = session.scalars(query).unique().all()
            for r in records:
                session.delete(r)
            # session.query(cls).filter(and_(*filters)).delete()
            session.flush()
        finally:
            session.commit()
            close_session(session)

    def execute_sql_query(sql_query):
        session = get_session()
        try:
            records = session.execute(sql_query)
            return records
        finally:
            close_session(session)


def create_diagram():
    graph: Dot = create_schema_graph(
        engine=get_engine(),
        metadata=Base.metadata,
        show_datatypes=True,
        show_indexes=True,
        rankdir="LR",
        show_column_keys=True,
    )
    graph.write_png("docs/_static/schema_diagram.png")


if __name__ == "__main__":
    create_diagram()
