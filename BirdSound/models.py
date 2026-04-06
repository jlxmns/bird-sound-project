from django.contrib.auth.models import AbstractUser
from django.db import models

from DjangoProject import settings


class User(AbstractUser):
    class Role(models.TextChoices):
        VIEWER = "leitor", "Leitor"
        BIOLOGIST = "biologo", "Biólogo"
        RESEARCHER = "pesquisador", "Pesquisador"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Bird(models.Model):
    common_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, unique=True)
    order = models.CharField(max_length=100, blank=True)
    family = models.CharField(max_length=100, blank=True)

    wingspan = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    length = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    habitat = models.TextField(blank=True)
    conservation_status = models.CharField(max_length=50, blank=True)

    image = models.ImageField(upload_to="birds/", null=True, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["common_name"]

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"


class IdentificationReport(models.Model):
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reports",
    )
    audio_file = models.FileField(upload_to="audio_uploads/")
    recorded_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Status(models.TextChoices):
        PENDING = "pending", "Não processado"
        PROCESSING = "processing", "Em processo"
        DONE = "done", "Processado"
        FAILED = "failed", "Falha de processamento"

    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report #{self.pk} by {self.submitted_by}"


class IdentificationResult(models.Model):
    report = models.ForeignKey(
        IdentificationReport, on_delete=models.CASCADE, related_name="results"
    )
    bird = models.ForeignKey(
        Bird, on_delete=models.SET_NULL, null=True, related_name="identifications"
    )
    confidence = models.FloatField()
    time_start = models.FloatField()
    time_end = models.FloatField()

    class Meta:
        ordering = ["-confidence"]
