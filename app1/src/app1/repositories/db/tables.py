import os

import sqlalchemy

from ...helpers.json import custom_json_deserializer, custom_json_serializer

# SQLAlchemy specific code, as with any other app
DATABASE_URL = os.environ.get("DB_URL", "sqlite:///./test.db")
# DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

metadata = sqlalchemy.MetaData()


engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args=(
        {} if "postgres" in DATABASE_URL else {"check_same_thread": False}
    ),
    json_serializer=custom_json_serializer,
    json_deserializer=custom_json_deserializer,
)


def get_audit_columns():
    audit_columns = [
        sqlalchemy.Column("is_active", sqlalchemy.Boolean),
        sqlalchemy.Column("reason", sqlalchemy.String),
        sqlalchemy.Column("created_by", sqlalchemy.String),
        sqlalchemy.Column(
            "created_on",
            sqlalchemy.DateTime,
            server_default=sqlalchemy.func.now(),
        ),
        sqlalchemy.Column("modified_by", sqlalchemy.String),
        sqlalchemy.Column("modified_on", sqlalchemy.DateTime),
    ]
    return audit_columns


tbl_configs = sqlalchemy.Table(
    "configs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("namespace", sqlalchemy.String),
    sqlalchemy.Column("config_code", sqlalchemy.String),
    sqlalchemy.Column("value", sqlalchemy.JSON),
    sqlalchemy.Column("as_of", sqlalchemy.Date),
    *get_audit_columns(),
)