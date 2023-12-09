import logging
import traceback

import utilities.database.database as db
import utilities.logger.log_sql as sq


class SQLAlchemyHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.database = db.Database()

    """ basic class overrides emit from Handler """
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc(exc)
        log = sq.Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'],
        )
        # session = sq.loadSession()
        # session.add(log)
        # session.commit()
        log_tbl = db.get_Table('log')
        self.database.insert(log_tbl.insert().values(log))