import alembic.config

alembic_args = [
    "--raiseerr",
    "upgrade",
    "head",
]


def db_migrate_handler(event, context):
    alembic.config.main(argv=alembic_args)
