from django_bolt import BoltAPI
from django_bolt.views import ModelViewSet

from BirdSound.models import Bird
from BirdSound.schemas import BirdSerializer

api = BoltAPI()

@api.viewset("/birds")
class BirdViewSet(ModelViewSet):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer

    async def list(self, request):
        """GET /birds"""
        birds = []
        async for bird in await self.get_queryset():
            birds.append(BirdSerializer.fields("list").from_model(bird))
        return birds

    async def retrieve(self, request, pk: int):
        """GET /birds/{pk}"""
        bird = await self.get_object(pk=pk)
        return BirdSerializer.from_model(bird)