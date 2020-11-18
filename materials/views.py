from rest_framework.generics import ListAPIView, get_object_or_404

from materials.models import Material, Recycler, MaterialAttribute
from materials.serializers import RecyclerSerializer, MaterialAttributeSerializer


class RecyclerListAPIView(ListAPIView):
    queryset = Recycler.objects.all()
    serializer_class = RecyclerSerializer

    def get_queryset(self):
        return self.queryset.prefetch_related(
            'recyclerquality_set', 'recyclerquality_set__material',
            'recyclerquality_set__material__materialattribute_set',
        )


class AttributesListAPIView(ListAPIView):
    queryset = MaterialAttribute.objects.all()
    serializer_class = MaterialAttributeSerializer

    def get_queryset(self):
        material = get_object_or_404(Material, pk=self.kwargs.get('material_id'))
        return self.queryset.filter(material=material)
