from django.core.management import BaseCommand

from materials.constants import ATTR_VALUE_TYPE
from materials.models import MaterialAttribute, AttributeOption, Attribute, Material, Recycler, RecyclerQuality

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


class Command(BaseCommand):
    def handle(self, *args, **options):
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
                'operator': 'eq',
                'operands': [
                    'ATTR_POLYESTER',
                    0.7
                ]
            },
            {
                'operator': 'eq',
                'operands': [
                    'ATTR_COTTON',
                    0.3
                ]
            }
        ]

        self.recycler = Recycler.objects.create(name='Recycler 1')

        self.quality = RecyclerQuality.objects.create(material=self.material, recycler=self.recycler,
                                                      title='Quality Best',
                                                      min_count=1, operations=self.operations)
