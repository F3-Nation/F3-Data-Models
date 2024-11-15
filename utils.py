import os
from dataclasses import dataclass
from typing import List, Tuple, TypeVar

import pg8000
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy import and_

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from models import Base


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

    if os.environ.get("USE_GCP", False):
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


def get_session(echo=False):
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


class DbManager:
    def get_record(cls: T, id) -> T:
        session = get_session()
        try:
            x = session.query(cls).filter(cls.get_id() == id).first()
            if x:
                session.expunge(x)
            return x
        finally:
            session.rollback()
            close_session(session)

    def find_records(cls: T, filters) -> List[T]:
        session = get_session()
        try:
            records = session.query(cls).filter(and_(*filters)).all()
            for r in records:
                session.expunge(r)
            return records
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

    def delete_records(cls: T, filters):
        session = get_session()
        try:
            session.query(cls).filter(and_(*filters)).delete()
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
