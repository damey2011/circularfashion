from decimal import Decimal
from typing import Union, Tuple, Any, List

from django.db import models
from django.db.models import JSONField, Sum
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from materials.constants import ATTR_VALUE_TYPES, ATTR_VALUE_TYPE, BOOLEAN_OPERATOR_CHOICES
from materials.exceptions import MissingOperatorException, MissingOperandsException, InvalidOperandException, \
    InvalidRootOperatorException, NoOperationToPerformException, UnTrustedOperationException


def make_placeholder(name: str) -> str:
    char_arr = []
    for item in name:
        if item.isalpha() or item.isnumeric():
            char_arr.append(item.upper())
        elif item == ' ':
            char_arr.append('_')
    return ''.join(char_arr)


class Attribute(MPTTModel):
    category = TreeForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=50, unique=True)
    placeholder = models.CharField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, **kwargs):
        self.placeholder = make_placeholder(self.name)
        super().save(**kwargs)

    class MPTTMeta:
        parent_attr = 'category'

    class Meta:
        ordering = ('category__name',)
        unique_together = ('category', 'name',)


class AttributeOption(models.Model):
    name = models.CharField(max_length=100, unique=True)
    placeholder = models.CharField(max_length=100, null=True, blank=True, unique=True)
    valid_for = models.ManyToManyField(Attribute, help_text='Choice is valid for what attributes')

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.placeholder = make_placeholder(self.name)
        super().save(**kwargs)


class Material(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MaterialAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    value_type = models.CharField(max_length=20, choices=ATTR_VALUE_TYPES)
    choice = models.ForeignKey(AttributeOption, null=True, blank=True, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    @property
    def value(self):
        return self.choice.name if self.value_type == ATTR_VALUE_TYPE.CHOICE else Decimal(self.percentage / 100)

    def __str__(self):
        return f'{str(self.material)} - {str(self.attribute)}'

    class Meta:
        unique_together = ('attribute', 'material',)


class Recycler(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class RecyclerQuality(models.Model):
    title = models.CharField(max_length=20)
    recycler = models.ForeignKey(Recycler, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    min_count = models.IntegerField(
        default=1,
        help_text='Minimum number of operations to be satisfied, -1 means all available conditions must be satisfied'
    )
    operations = JSONField(default=list)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'recycler',)

    def translate_operand(self, operand: Union[str, int, float]) -> Any:
        if isinstance(operand, str) and not operand.isnumeric():
            qs = None
            is_attribute = False
            if operand.startswith('ATTR_'):
                operand = operand.replace('ATTR_', '', 1)
                is_attribute = True
                qs = MaterialAttribute.objects.filter(material=self.material, attribute__placeholder=operand)
            elif operand.startswith('OPT_'):
                operand = operand.replace('OPT_', '', 1)
                is_attribute = False
                qs = MaterialAttribute.objects.filter(
                    material=self.material, choice__placeholder=operand
                )
            if not qs:
                raise InvalidOperandException(operand)
            right_attribute: MaterialAttribute = qs.first()
            if is_attribute:
                if not right_attribute.attribute.category:
                    # No category means it a cumulative operation
                    return MaterialAttribute.objects.filter(
                        value_type=ATTR_VALUE_TYPE.PERCENTAGE, material=self.material
                    ).aggregate(sum=Sum('percentage')).get('sum', 0)
            return right_attribute.value
        else:
            return operand

    def expression_to_python(self, expression: dict, is_root: bool = True) -> Tuple[str, str]:
        """
        Expressions need to be in the format:
        [
            {
                operator: '+',
                operands: [
                    {
                        operator: '*',
                        operands: [9, 10]
                    },
                    10,
                    'OTHER_CELLULOSICS'
                ]
            }
        ]
        """
        boolean_operators = [op[1] for op in BOOLEAN_OPERATOR_CHOICES]
        operator = expression.get('operator')
        if not operator:
            raise MissingOperatorException(expression)
        elif is_root and operator not in boolean_operators:
            raise InvalidRootOperatorException(operator)
        operands = expression.get('operands', [])
        if not operands:
            raise MissingOperandsException(expression)
        code = "("
        readable_code = "("
        for operand in operands:
            if isinstance(operand, dict):
                operand_code, operand_readable_code = self.expression_to_python(expression=operand, is_root=False)
                readable_code += operand_readable_code
            else:
                readable_code += str(operand)
                operand_code = self.translate_operand(operand)
            code += f'"{operand_code}"' if isinstance(operand_code, str) else f'{str(operand_code)}'
            code += f' {operator} '
            readable_code += f' {operator} '
        code = code.rstrip(f' {operator} ')
        readable_code = readable_code.rstrip(f' {operator} ')
        code += ")"
        readable_code += ")"
        if operator in boolean_operators:
            code = f'bool({code})'
        return code, readable_code

    def evaluate_conditions(self, readable: bool = False) -> List[Any]:
        res = []
        safe_names = {'bool': bool}
        for operation in self.operations:
            code, readable_exp = self.expression_to_python(operation)
            if not readable:
                code = compile(code, '<string>', 'eval')
                for name in code.co_names:
                    if name not in safe_names:
                        raise UnTrustedOperationException(code.co_names)
                code = eval(code, {"__builtins__": {}}, safe_names)
                res.append(code)
            else:
                res.append(readable_exp)
        return res

    def judge(self) -> bool:
        """
        - If the attribute passed in is a parent attribute (category), then we should do an cummulation
        - If the operand is on the left, we would check the attribute
        - If the operand is on the right side, we would check in order (attribute_options, free_input)
        - Substitute all the placeholders and use python evaluate
        """
        if not self.operations or not isinstance(self.operations, list):
            raise NoOperationToPerformException(self.operations)
        res = self.evaluate_conditions()
        if self.min_count == -1:
            return all(res)
        return res.count(True) >= self.min_count
