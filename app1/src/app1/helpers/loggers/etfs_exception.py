class ETFSException(Exception):
    '''
    Base class for other exceptions
    '''
    pass

    def __init__(self, message, *args, **kwargs):
        self.message = message
        self.args = [a for a in args]

    def __str__(self):
        ret_data = f"{self.message}. args >>> {self.args}"
        return ret_data



class InvalidArguements(ETFSException):
    '''
    raised when invalid number of arguements are passed to a calling script
    '''
    pass

class NoRowsFound(ETFSException):
    '''
    raised when a db query finds now rows
    '''
    pass

class ConnectionError(ETFSException):
    '''
    raised when database connection fails
    '''
    pass

class MissingCurrencyInDB(ETFSException):
    '''
    raised when wmr csv file has unmapped currencies
    '''

    def __init__(self, currencies):
        self.missing_currencies = currencies

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: " \
                   f"The following currencies {self.missing_currencies} " \
                   f"are missing in database."

        return ret_data

    pass


class NullValuesFound(ETFSException):
    """
    raised when null values are found
    """
    pass


class FileException(Exception):
    def __init__(self, file_name):
        self.file_name = file_name

    pass


class FileNotFound(FileException):
    """
    raised when a file to be processed is not found
    """
    pass


class MissingColumn(FileException):
    """
    raised when a column is missing
    """

    def __init__(self, columns):
        self.missing_columns = columns
        # super().__init__(file_name)

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: Column(s) {self.missing_columns} are missing."

        return ret_data

    pass


class InvalidType(FileException):
    """
    raised when the type of a column is not as what is expected
    """

    def __init__(self, column_name, column_type):
        self.column_name = column_name
        self.column_type = column_type

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: Column [{self.column_name}] has invalid type, it should be [{self.column_type}]"
        return ret_data

    pass


class MissingValue(FileException):
    """
    raised when the value of a column is missing
    """

    def __init__(self, column_name):
        self.column_name = column_name

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: Some of the value(s) are missing in column [{self.column_name}]"
        return ret_data

    pass


class DataFrame_Empty(ETFSException):

    def __init__(self, *args):
        self.args = [a for a in args]

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: No data retrieved in data frame. {self.args}"
        return ret_data

    pass


class DataFrame_Unequal(ETFSException):

    def __init__(self, *args):
        self.args = [a for a in args]

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: Dataframes compared do not match each other. {self.args}"
        return ret_data

    pass


class MissingValues(ETFSException):

    def __init__(self, *args):
        self.args = [a for a in args]

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: Missing values. {self.args}"
        return ret_data

    pass


class Data_Mismatch(ETFSException):

    def __init__(self, *args):
        self.args = [a for a in args]

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: Data values are not matching when compared. {self.args}"
        return ret_data

    pass

class List_Convert(ETFSException):

    def __init__(self, *args):
        self.args = [a for a in args]

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: Unable to convert to list. {self.args}"
        return ret_data

    pass

class Run_Dates_Mismatch(ETFSException):

    def __init__(self, *args):
        self.args = [a for a in args]

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: Run dates not covered. {self.args}"
        return ret_data

    pass

class Data_Transform(ETFSException):

    def __init__(self, *args):
        self.args = [a for a in args]

    def __str__(self):
        ret_data = f"<<Exception : {self.__class__.__name__}>> :: Error during transformation. {self.args}"
        return ret_data

    pass