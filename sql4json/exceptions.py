class SQLStatementFormatException(Exception):
    def __init__(self, message):
        super(SQLStatementFormatException, self).__init__(message)


class FromClauseException(SQLStatementFormatException):
    def __init__(self, message):
        super(FromClauseException, self).__init__(message)


class WhereClauseException(SQLStatementFormatException):
    def __init__(self, message):
        super(WhereClauseException, self).__init__(message)


class LimitClauseException(SQLStatementFormatException):
    def __init__(self, message):
        super(LimitClauseException, self).__init__(message)