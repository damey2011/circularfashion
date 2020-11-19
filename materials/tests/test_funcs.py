from django.test import TestCase

from materials.constants import ATTR_VALUE_TYPE
from materials.exceptions import NoOperationToPerformException
from materials.models import Material, Attribute, MaterialAttribute, Recycler, AttributeOption, \
    RecyclerQuality

CATEGORIES = {
    'Composition': """
        Cotton
        Polyester
        Wool
        Cashmere
        Viscose/Lyocell
        Nylon
        Polyamide
        Acrylic 
        Elastane 
        Silk 
        Down
        Leather
        Other cellulosics
        Others
        """,
    'Fabric Construction': """
        Type
    """,
    'Colour Shade': """
        Light/dark
    """,
    'Dyes': """
        Dye method
        Dye stuff
    """
}

OPTIONS = {
    'Fabric Construction': """
        Yarns
        Thread
        Woven
        Knitted
        Nonwoven
        Any
    """,
    'Colour Shade': """
        light
        dark
        mixed
        unspecified
    """,
    'Dye method': """
        Undyed
        Unspecified
        Direct Dyed
        Top Dyed
        Yarn Dyed
        Dope Dyed
        Piece Dyed
    """,
    'Dye stuff': """
        Reactive Dyes
        Synthetic Pigments
        Natural Pigments
        Pastes
    """
}


class TestSetup(TestCase):
    def setUp(self) -> None:
        self.material = Material.objects.create(name='Material 1')

        attributes = []

        for k, v in CATEGORIES.items():
            category = Attribute.objects.create(name=k)
            for a in v.strip().split('\n'):
                attr = Attribute.objects.create(name=a.title().strip(), category=category)
                # create the options of the attribute if they have options
                # if you cannot find options for the sub-category, check if the parent category has options
                for o in OPTIONS.get(a.strip(), OPTIONS.get(k, '')).strip().split('\n'):
                    ao, _ = AttributeOption.objects.get_or_create(name=o.title().strip())
                    ao.valid_for.add(attr)
                attributes.append(attr)

        material_attributes = []
        for attr in attributes:
            # the composition category is the only one with numerical input, the rest are choice attributes
            value_type = ATTR_VALUE_TYPE.PERCENTAGE if attr.category.name == 'Composition' else ATTR_VALUE_TYPE.CHOICE
            material_attributes.append(MaterialAttribute(material=self.material, attribute=attr, value_type=value_type))
        MaterialAttribute.objects.bulk_create(material_attributes)

        # seed the material attributes with some options and values
        polyester = MaterialAttribute.objects.get(material=self.material, attribute__name='Polyester')
        polyester.percentage = 70.00
        polyester.save()

        cotton = MaterialAttribute.objects.get(material=self.material, attribute__name='Cotton')
        cotton.percentage = 30.00
        cotton.save()

        self.operations = [
            {
                'operator': 'and',
                'operands': [
                    4,
                    {
                        'operator': '*',
                        'operands': [8, 8, 8]
                    },
                    'ATTR_POLYESTER'
                ]
            }
        ]

        self.recycler = Recycler.objects.create(name='Recycler 1')

    def create_quality(self):
        self.quality = RecyclerQuality.objects.create(material=self.material, recycler=self.recycler,
                                                      title='Quality Best',
                                                      min_count=1, operations=self.operations)


class TestGeneral(TestSetup):
    def test_that_non_list_operation_raises_exception(self):
        self.operations = {
            'operator': 'and',
            'operands': [
                4,
                {
                    'operator': '*',
                    'operands': [8, 8, 8]
                },
                'ATTR_POLYESTER'
            ]
        }
        with self.assertRaises(NoOperationToPerformException):
            self.create_quality()
            self.quality.judge()

    def test_that_cumulative_operation_returns_valid_response(self):
        self.operations = [{
            'operator': '==',
            'operands': [
                'CUM_COMPOSITION',
                1
            ]
        }]
        self.create_quality()
        self.assertEqual(self.quality.judge(), True)

    def test_that_choice_based_operation_returns_valid_data(self):
        self.operations = [{
            'operator': '==',
            'operands': [
                'ATTR_DYE_STUFF',
                'OPT_TOP_DYED'
            ]
        }]
