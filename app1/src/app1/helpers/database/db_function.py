import pandas
from sqlalchemy import and_, bindparam
from sqlalchemy import select, func, case

# local imports
import utilities.database.database as db

# variable
database = db.Database('')

# methods
def select_import_file_type(file_name=None, file_id=None):
    """
    Use this function to get the import file id given a file type name or a file type id

    :param file_name: name of the input file type
    :param file_id: id of the input file type
    :return: row (list) of matching record from import file type table
    """
    if file_name is not None:
        import_file_type = database.get_Table('import_file_type')
        import_file_type = import_file_type.select().where(and_(import_file_type.c.file_name == file_name,
                                                                import_file_type.c.is_deleted==0,
                                                                import_file_type.c.is_suspended==0))
        result = database.select(import_file_type)

    elif file_id is not None:
        import_file_type = database.get_Table('import_file_type')
        import_file_type = import_file_type.select().where(and_(import_file_type.c.import_file_type_id == file_id,
                                                                import_file_type.c.is_deleted == 0,
                                                                import_file_type.c.is_suspended == 0))
        result = database.select(import_file_type)

    else:
        import_file_type = database.get_Table('import_file_type')
        import_file_type = import_file_type.select().where(and_(import_file_type.c.is_deleted == 0,
                                                                import_file_type.c.is_suspended == 0))
        result = database.select(import_file_type)


    return result

def select_import_file_type_id(name):
    """
    This function will return bank id of the provided bank name

    :param bank_name: string
    :return: bank id : int
    """
    tbl_import_file_type = database.get_Table('import_file_type')

    select_stmt = select([tbl_import_file_type.c.import_file_type_id]).where(
        and_(tbl_import_file_type.c.is_deleted == 0,
             tbl_import_file_type.c.is_suspended == 0,
             tbl_import_file_type.c.file_name == name))

    # result = database.select(select_stmt)
    # print(select_stmt)
    result = database.select_query_data_frame(select_stmt=select_stmt)

    if len(result) == 1:
        return int(result['import_file_type_id'][0])
    else:
        return None

def insert_into_import_file(record):
    """
    Inserts a new record into import file table to create a log and returns the row id
    (import_file_id)

    :param record: record to insert into import file table
    :return: import file id
    """
    import_file = database.get_Table('import_file')
    import_file_insert_stmt = import_file.insert().values(record) #.returning(import_file.c.import_file_id)
    pk_import_file_id = database.insert(import_file_insert_stmt)
    return pk_import_file_id
    # for row in pk_import_file_id:
    #     row_dict = dict(row)
    #     print(row_dict)

def is_file_processed(file_type_id=None, file_date=None, file_name=None):
    """
    Checks if a file has been processed by using either (a) File Type ID and Run Date, or (b) File Name
    Both these parameters must be setup in Import File Type table

    :param import_file_type_id: Import File ID from Import File Type table
    :param file_date: Date to check against file_date of Import File table
    :param file_name: Import File name from Import File table
    :return: integer (True for file exists, False if not exist)
    """
    tbl_import_file = database.get_Table('import_file')

    # compose the query
    import_file_select_stmt = tbl_import_file.select().where(and_(tbl_import_file.c.is_deleted == 0,
                                                                  tbl_import_file.c.is_suspended == 0))

    if file_type_id and file_date:
        import_file_select_stmt = import_file_select_stmt.where(
            and_(tbl_import_file.c.import_file_type_id == file_type_id))

    if file_date:
        import_file_select_stmt = import_file_select_stmt.where(
            and_(func.date(tbl_import_file.c.file_date) == file_date))

    if file_name:
        import_file_select_stmt = import_file_select_stmt.where(and_(tbl_import_file.c.file_name == file_name))

    # execute the query
    result = database.select(import_file_select_stmt)

    # return the result
    if (len(result) > 0):
        return True

    return False

def update_dispatched_file_log(record):
    """
    update the existing record(s) in dispatched_file_log

    :param record: record which needs to be updated
    :return:
    """
    # get the table definition
    tbl_dispatched_file_log = database.get_Table('dispatched_file_log')

    # prepare the update statement
    update_stmt = tbl_dispatched_file_log.update(). \
        where(tbl_dispatched_file_log.c.dispatched_file_log_id == bindparam('wp_dispatched_file_log_id')). \
        values(is_deleted=1, is_suspended=1, modified_by=bindparam('UserName'), modified_on='now()')

    # execute the statement
    row_affected = database.update_multiple(update_stmt, record)

    # return the data
    return row_affected
