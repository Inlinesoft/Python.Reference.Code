from pricers.application.services.uow import UnitOfWork


class DbUnitOfWork(UnitOfWork):
    def __init__(self, engine):
        self.engine = engine

    def refresh_repos(self, conn):
        for repo in self.repos:
            repo.conn = conn

    def __enter__(self):
        # Use a single connection when entering the context manager
        self.conn = self.engine.connect()
        self.refresh_repos(self.conn)
        self.tran = self.conn.begin()
        return self

    def __exit__(self, *args):
        self.rollback()
        self.conn.close()
        # switch back to the engine
        self.refresh_repos(self.engine)

    def commit(self):
        self.tran.commit()

    def rollback(self):
        self.tran.rollback()
