from collections import namedtuple
from functools import reduce

AttrCat = namedtuple(
    'AttrCat', ['COLOR_SHADE', 'COLOR', 'DYE_METHOD', 'DYE_STUFF', 'PRINT_AND_PATTERN', 'PRINT_STUFF', 'FINISHES',
                'COMPLIANCE_STANDARDS', 'TRIMS', 'FABRIC_CONSTRUCTION']
)('color_shade', 'color', 'dye_method', 'dye_stuff', 'print_and_pattern', 'print_stuff', 'finishes',
  'compliance_standards', 'trims', 'fabric_construction')

ATTR_VALUE_TYPE = namedtuple('AttrValueType', ['PERCENTAGE', 'CHOICE'])('p', 'c')
ATTR_VALUE_TYPES = (
    (ATTR_VALUE_TYPE.PERCENTAGE, 'Percentage'),
    (ATTR_VALUE_TYPE.CHOICE, 'Choice')
)

OPERAND_DATA_TYPE = namedtuple('OperandType', ['NUMBER', 'STRING', 'OPERATION'])('number', 'string', 'operation')
OPERAND_DATA_TYPES = (
    (OPERAND_DATA_TYPE.NUMBER, 'Number'),
    (OPERAND_DATA_TYPE.STRING, 'String'),
    (OPERAND_DATA_TYPE.OPERATION, 'Operation'),
)

OPERATORS = dict(
    ADD={
        'text': 'add',
        'sign': '+',
        'is_boolean': False
    },
    MUL={
        'text': 'mul',
        'sign': '*',
        'is_boolean': False
    },
    AND={
        'text': 'and',
        'sign': 'and',
        'is_boolean': True
    },
    OR={
        'text': 'or',
        'sign': 'or',
        'is_boolean': True
    },
    GT={
        'text': 'gt',
        'sign': '>',
        'is_boolean': True
    },
    LT={
        'text': 'lt',
        'sign': '<',
        'is_boolean': True
    },
    GTE={
        'text': 'gte',
        'sign': '>=',
        'is_boolean': True
    },
    LTE={
        'text': 'lte',
        'sign': '<=',
        'is_boolean': True
    },
    EQ={
        'text': 'eq',
        'sign': '==',
        'is_boolean': True
    },
    NEQ={
        'text': 'neq',
        'sign': '!=',
        'is_boolean': True
    }
)

OPERATOR_CHOICES = tuple([(key, val.get('sign')) for key, val in OPERATORS.items()])
BOOLEAN_OPERATOR_CHOICES = tuple([(key, val.get('sign')) for key, val in OPERATORS.items() if val.get('is_boolean')])

OPERAND_TYPE = namedtuple('OperandType', [
    'ATTRIBUTE', 'OPERATION', 'TEXT_INPUT', 'NUMBER_INPUT', 'NULL', 'BOOLEAN_INPUT', 'OPTION', 'CUMMULATIVE'
])(
    'attribute', 'operation', 'text_input', 'number_input', 'null', 'boolean', 'option', 'cummulative'
)
OPERAND_TYPES = (
    (OPERAND_TYPE.ATTRIBUTE, 'Material Attribute'),
    (OPERAND_TYPE.OPERATION, 'Operation'),
    (OPERAND_TYPE.TEXT_INPUT, 'Text Input'),
    (OPERAND_TYPE.NUMBER_INPUT, 'Number Input'),
    (OPERAND_TYPE.NULL, 'Null'),
    (OPERAND_TYPE.BOOLEAN_INPUT, 'Boolean'),
    (OPERAND_TYPE.OPTION, 'Option'),
    (OPERAND_TYPE.CUMMULATIVE, 'Category Cummulative'),
)

OPERAND_POSITION = namedtuple('OperandPosition', ['LEFT', 'RIGHT', 'NOT_REQUIRED'])(0, 1, 2)
OPERAND_POSITIONS = (
    (OPERAND_POSITION.LEFT, 'Left'),
    (OPERAND_POSITION.RIGHT, 'Right'),
    (OPERAND_POSITION.NOT_REQUIRED, 'Not Required'),
)
