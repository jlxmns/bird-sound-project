from django_bolt import BoltAPI, FileSize, UploadFile
from django_bolt.shortcuts import render
from django_bolt.types import Request
from django_bolt.views import ModelViewSet
from django_bolt.param_functions import Form, File
from typing import Annotated

from BirdSound.models import Bird
from BirdSound.schemas import BirdSerializer, CreateBirdSerializer, UpdateBirdSerializer

api = BoltAPI()
api.mount_django("/media", clear_root_path=True)


@api.get("/")
async def index(request: Request):
    return render(request, "BirdSound/bird-list.html")


@api.get("/bird/{pk}")
async def bird_detail(request: Request, pk: int):
    return render(request, "BirdSound/bird-detail.html", {"pk": pk})


@api.get("/bird/add")
async def bird_add(request: Request):
    return render(request, "BirdSound/bird-add.html")


@api.viewset("/birds")
class BirdViewSet(ModelViewSet):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer
    list_serializer_class = BirdSerializer.fields("list")

    async def list(self, request: Request):
        """GET /birds"""
        birds = []
        async for bird in await self.get_queryset():
            birds.append(self.serialize(bird))
        return birds

    async def retrieve(self, request: Request, pk: int):
        """GET /birds/{pk}"""
        bird = await self.get_object(pk=pk)
        return self.serialize(bird)

    async def create(
        self,
        request: Request,
        data: Annotated[CreateBirdSerializer, Form()],
        file: Annotated[
            UploadFile | None, File(max_size=FileSize.MB_50, allowed_types="image/*")
        ] = None,
    ):
        """POST /birds - create a new bird"""
        bird = Bird(**data.dump(exclude_unset=True))
        if file:
            bird.image = file.file
        await bird.asave()
        return self.serialize(bird)

    async def update(
        self,
        request: Request,
        pk: int,
        data: Annotated[UpdateBirdSerializer, Form()],
        file: Annotated[
            UploadFile | None, File(max_size=FileSize.MB_50, allowed_types="image/*")
        ] = None,
    ):
        """PUT /birds/{pk} - Update a bird"""
        bird = await self.get_object(pk)
        for k, v in data.dump(exclude_unset=True).items():
            if v is not None:
                setattr(bird, k, v)
        if file:
            bird.image = file.file
        await bird.asave()
        return self.serialize(bird)

    async def partial_update(
        self,
        request: Request,
        pk: int,
        data: Annotated[UpdateBirdSerializer, Form()],
        file: Annotated[
            UploadFile | None, File(max_size=FileSize.MB_50, allowed_types="image/*")
        ] = None,
    ):
        """PATCH /birds/{pk} - Partially update a bird."""
        bird = await self.get_object(pk)
        for k, v in data.dump(exclude_unset=True).items():
            if v is not None:
                setattr(bird, k, v)
        if file:
            bird.image = file.file
        await bird.asave()
        return self.serialize(bird)

    async def destroy(self, request: Request, pk: int):
        """DELETE /birds/{pk} - Delete a birds."""
        bird = await self.get_object(pk=pk)
        await bird.adelete()
        return {"deleted": True}

    def serialize(self, bird: Bird):
        result = self.serializer_class.from_model(bird).dump()
        result["image"] = bird.image.url if bird.image else None
        return result
