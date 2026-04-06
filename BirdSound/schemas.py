from django_bolt.serializers import Serializer

class BirdSerializer(Serializer):
    id: int
    common_name: str
    scientific_name: str
    order: str | None = None
    family: str | None = None

    wingspan: float | None = None
    weight: float | None = None
    length: float | None = None

    habitat: str | None = None
    conservation_status: str | None = None

    image: str | None = None
    description: str | None = None

    class Config:
        field_sets = {
            "list": ["id", "common_name", "scientific_name", "habitat", "conservation_status"],
        }