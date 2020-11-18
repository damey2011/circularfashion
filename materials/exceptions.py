from materials.constants import OPERATOR_CHOICES, BOOLEAN_OPERATOR_CHOICES


class MissingOperatorException(BaseException):
    def __init__(self, expression, *args):
        self.message = f'Operator not present in expression {str(expression)}. ' \
                       f'Operators [{", ".join([op[1] for op in OPERATOR_CHOICES])}] are allowed.'
        super().__init__(self.message, *args)


class MissingOperandsException(BaseException):
    def __init__(self, expression, *args):
        self.message = f'Operands not present in expression {str(expression)}.'
        super().__init__(self.message, *args)


class InvalidOperandException(BaseException):
    def __init__(self, operand, *args):
        self.message = f'Invalid operand {str(operand)}.'
        super().__init__(self.message, *args)


class InvalidRootOperatorException(BaseException):
    def __init__(self, operator, *args):
        self.message = f'Invalid root operator "{str(operator)}". ' \
                       f'Root operator must be a function that returns a boolean. ' \
                       f'\nSupported boolean operations are ' \
                       f'[{", ".join([op[1] for op in BOOLEAN_OPERATOR_CHOICES])}]'
        super().__init__(self.message, *args)


class NoOperationToPerformException(BaseException):
    def __init__(self, operations, *args):
        self.message = f'No operation to perform or invalid expressions. \n{str(operations)}'
        super().__init__(self.message, *args)


class UnTrustedOperationException(BaseException):
    def __init__(self, co_names, *args):
        self.message = f'Untrusted operation. Found [{", ".join(co_names)}]'
        super().__init__(self.message, *args)