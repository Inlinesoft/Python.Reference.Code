import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from config.definitions import DB_SRVR_CONN
#from config.definitions import common
from config import definitions
from utilities import DB_ENABLE_LOGGING

pd.set_option('display.precision',7)

"""
#----------------------------------------------------------------
# Name:         database.py
# Purpose:      Establish connection to the database
#               and enable basic database operations like (select,
#               insert, etc.)
# Author:       
#----------------------------------------------------------------
"""


class Database:
    __dbEngine = None
    __db_conn_str = None

    def __init__(self):
        self.__init__(definitions.common['DB_SRVR_CONN'])

    def __init__(self, database_con_str=None):
        self.__dbEngine = None

        if (database_con_str):
            self.__db_conn_str = database_con_str
        else:
            self.__db_conn_str = definitions.common['DB_SRVR_CONN']

            # print(f"__init__ :{self.__db_conn_str}")

    def __del__(self):
        try:
            self.dispose_engine()
            #print("destroy")
        except Exception as e:
            print('')

    def create_engine(self, database_con_str=None):
        """
        Establish the connection with the database and initialize
        the local variable engine.
        :return:
        """
        # print (f"Create Engine :{self.__db_conn_str}")
        if self.__dbEngine== None:
            self.__dbEngine = create_engine(self.__db_conn_str, echo=DB_ENABLE_LOGGING, pool_size=20,
                                            max_overflow=0)  # , poolclass=QueuePool
            self.__Base = declarative_base(self.__dbEngine)

    def dispose_engine(self):
        """
        Establish the connection with the database and initialize
        the local variable engine.
        :return:
        """
        if self.__dbEngine != None:
            self.__dbEngine.dispose()

    def get_engine(self):
        """
        check either the db engine's instance has been created
        or not, if not then call db_create_engine to create the
        database engine and then return the instance if it's
        already been instantiated then just return the variable
        self.__dbEngine
        :input:
                self
        :return:
                self.__dbEngine
        """
        if self.__dbEngine == None:
            self.create_engine()

        return self.__dbEngine

    def create_session(self):
        """
        Create a db session if one doesn't exist already. New
        session is created by calling the get_engine. If already
        instantiated, simply returns sessions object
        :return:
                self.__session
        """
        if self.__session == None:
            self.__engine = self.get_engine()
            __metadata = self.__Base.metadata
            __Session = sessionmaker(bind=self.__engine)
            self.__session = __Session()

        return self.__session

    def get_connection(self):
        """
        get the connection object
        :input :
                self
        :return:
                connection object
        """
        #check either the Engine object has already been instantiated
        #if not then do instansiate the engine
        if self.__dbEngine == None:
            self.create_engine()

        #Check either the conection is closed if it is then
        #connect to the database again
        #if self.__connection.closed():
        self.__connection = self.get_engine().connect()

        return self.__connection

    def get_metadata(self):
        """
        get the metaData object
        :return:
        """
        self.__metaData = MetaData(self.get_engine())
        return self.__metaData

    def start_transaction(self):
        """

        :return:
        """
        return self.get_connection().begin()

    def commit_transaction(self, trans):
        """

        :return:
        """
        trans.commit()

    def rollback_transaction(self, transaction):
        """

        :return:
        """
        transaction.rollback()

    """***********************************************************************************
    ***                                     DDL                                        ***            
    ***********************************************************************************"""
    def get_Table(self, tableName):
        return Table(tableName,
                     self.get_metadata(),
                     autoload=True,
                     autoload_with=self.get_engine())


    """***********************************************************************************
    ***                                     DML                                        ***            
    ***********************************************************************************"""

    """
            Select Statement(s)
    """
    def select(self, statement):
        """

        :return:
        """
        returnData = []
        resultsProxy = self.get_connection().execute(statement)

        for item in resultsProxy.fetchall():
            info = {}
            for key in resultsProxy.keys():
                info[key] = item[key]
            returnData.append(info)

        return returnData

    """
            Select Statement PANDAS
    """

    def select_table_data_frame(self, tablename, ignore_invalid=True):
        """

        :return:
        """
        df = pd.read_sql_table(tablename, self.get_engine())
        # if ignore_invalid:
        #    df = df.loc[(df['is_suspended'] == 0) & (df['is_deleted'] == 0)]
        return df

    def select_query_data_frame(self, select_stmt):
        """

        :return:
        """
        df = pd.read_sql_query(select_stmt, self.get_engine())
        return df

    """
        Insert Statement with different parameters
    """
    def insert(self,stmt):
        """

        :return:
        """
        result = self.get_connection().execute(stmt)
        return result.inserted_primary_key[0]

    def insert_multiple(self,stmt, dataInListOfDict):
        """

        :return:
        """
        result = self.get_connection().execute(stmt, dataInListOfDict)
        return result.rowcount

    def insert_multipleUsingDF(self, stmt, dataFrame):
        """

        :return:
        """
        data = dataFrame.to_dict(orient='records')
        result = self.get_connection().execute(stmt, data)
        return result.rowcount

    """
        Insert table PANDAS
    """

    def insert_table_data_frame(self, tablename, df):
        """

        :return:
        """
        pd.DataFrame.to_sql(df, name=tablename, con=self.get_engine(), if_exists='append', index=False)
        return

    """
           Update statement(s) with different parameters
    """
    def update(self, stmt):
        """

        :return:
        """
        result = self.get_connection().execute(stmt)
        return result.rowcount

    def update_multiple(self, stmt, dataInListOfDict):
        """

        :return:
        """
        result = self.get_connection().execute(stmt,dataInListOfDict)
        return result.rowcount


    def update_multipleUsingDF(self, stmt, dataFrame):
        """

        :return:
        """
        data = dataFrame.to_dict(orient='records')
        result = self.get_connection().execute(stmt, data)
        return result.rowcount

    """
           Update statement(s) with different parameters
    """
    def delete(self, stmt):
        """

        :return:
        """
        return

    """
           Other's
    """
    def execute(self, stmt):
        """

        :return:
        """

        return

# if __name__ == "__main__":
#     pass
    # database = Database()
    # metadata = database.get_metadata()
    # import_file = database.get_Table('import_file')
    # forex_spot_history = database.get_Table('forex_spot_history')

    # select_import_file_stmt = select([import_file.c.import_file_type_id]). \
    #     where((and_(import_file.c.file_name == '.csv',
    #                 import_file.c.import_file_type_id == 103,
    #                 import_file.c.file_date == '2017-06-09 00:00:00',
    #                 import_file.c.is_suspended == 0,
    #                 import_file.c.is_deleted == 0,
    #                 import_file.c.import_file_id == forex_spot_history.import_file_id)))

    # update_history_stmt = forex_spot_history.update(). \
    #     where((and_(import_file.c.file_name == 'wmr0906.csv',
    #                 import_file.c.file_date == '2017-06-09 00:00:00',
    #                 import_file.c.is_suspended == 0,
    #                 import_file.c.is_deleted == 0,
    #                 import_file.c.import_file_id == forex_spot_history.c.import_file_id))). \
    #     values(is_suspended=1,
    #           is_deleted=1,
    #           modified_by='',
    #           modified_on='now()')
    # rows = database.update(update_forex_spot_history_stmt)
    # print(rows)