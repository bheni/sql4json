class BooleanExpressionException(Exception):
    def __init__(self, message):
        super(SQLStatementFormatException, self).__init__(message)

        self.error_message = message