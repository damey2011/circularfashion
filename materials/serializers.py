from rest_framework import serializers

from materials.models import Material, Recycler, RecyclerQuality, MaterialAttribute, Attribute, AttributeOption


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            'id',
            'name'
        )


class AttributeSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Attribute
        fields = (
            'id',
            'name',
            'placeholder',
            'category'
        )


class AttributeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeOption
        fields = (
            'id',
            'name',
            'placeholder'
        )


class MaterialAttributeSerializer(serializers.ModelSerializer):
    choice = AttributeOptionSerializer()
    attribute = AttributeSerializer()

    class Meta:
        model = MaterialAttribute
        fields = (
            'id',
            'attribute',
            'value_type',
            'choice',
            'percentage'
        )


class MaterialSerializer(serializers.ModelSerializer):
    attributes = serializers.HyperlinkedRelatedField(
        source='id', view_name='materials:attributes', lookup_url_kwarg='material_id', read_only=True
    )
    attributes_count = serializers.IntegerField(source='materialattribute_set.count', read_only=True)

    class Meta:
        model = Material
        fields = (
            'id',
            'name',
            'attributes',
            'attributes_count'
        )


class RecyclerQualitySerializer(serializers.ModelSerializer):
    material = MaterialSerializer()
    passed = serializers.BooleanField(source='judge')
    condition = serializers.SerializerMethodField()

    class Meta:
        model = RecyclerQuality
        fields = (
            'id',
            'title',
            'min_count',
            'material',
            'condition',
            'operations',
            'passed'
        )

    def get_condition(self, obj):
        return ' and '.join(obj.evaluate_conditions(readable=True))


class RecyclerSerializer(serializers.ModelSerializer):
    qualities = RecyclerQualitySerializer(source='recyclerquality_set', many=True)

    class Meta:
        model = Recycler
        fields = (
            'id',
            'name',
            'qualities'
        )
