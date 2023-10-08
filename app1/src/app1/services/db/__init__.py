import os

import inject

from app1 import repositories as repo
from app1.repositories.loaders import run_data_loaders
from app1.services.uow import UnitOfWork
from app1.repositories import db as db_repo # Infrastructure
from app1.services.db.uow import DbUnitOfWork # Infrastructure


def loadup_db():
    # when in CI we want to test alembic migration;
    # prevent re-creation of tables from repos
    if not os.environ.get("CI"):
        metadata = db_repo.metadata
        engine = db_repo.engine
        metadata.drop_all(bind=db_repo.engine)
        metadata.create_all(engine)

    run_data_loaders()


def db_deps_config(binder):
    engine = db_repo.engine
    (
        binder.bind(repo.ConfigsRepository, db_repo.DbConfigsRepository(engine))
        .bind(UnitOfWork, DbUnitOfWork(engine))
    )


def configure_dependencies():
    inject.configure_once(db_deps_config, bind_in_runtime=False)


def setup_and_load_db_repos():
    configure_dependencies()
    loadup_db()
