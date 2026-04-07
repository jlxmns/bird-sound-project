# yourapp/management/commands/seed_birds.py

import httpx
import os
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from BirdSound.models import Bird
from dotenv import load_dotenv

load_dotenv()

NUTHATCH_API_KEY = os.environ.get("NUTHATCH_API_KEY")


class Command(BaseCommand):
    help = "Seeds the database with 30 birds from the Nuthatch API"

    def handle(self, *args, **kwargs):
        if not NUTHATCH_API_KEY:
            raise CommandError("NUTHATCH_API_KEY is not set in your .env file.")

        self.stdout.write("Fetching birds from Nuthatch API...")

        response = httpx.get(
            "https://nuthatch.lastelm.software/v2/birds",
            headers={"API-Key": NUTHATCH_API_KEY},
            params={
                "pageSize": 30,
                "page": 1,
                "hasImg": True,
            },
        )
        response.raise_for_status()
        entities = response.json()["entities"]

        created = 0
        skipped = 0

        for b in entities:
            if Bird.objects.filter(scientific_name=b["sciName"]).exists():
                self.stdout.write(f"  Skipping (exists): {b['sciName']}")
                skipped += 1
                continue

            bird = Bird(
                common_name=b.get("name"),
                scientific_name=b.get("sciName"),
                order=b.get("order") or None,
                family=b.get("family") or None,
                conservation_status=b.get("status") or None,
                wingspan=b.get("wingspanMax") or None,
                length=b.get("lengthMax") or None,
            )

            images = b.get("images", [])
            if images and images[0]:
                image_url = images[0]
                try:
                    img_response = httpx.get(
                        image_url, timeout=15, follow_redirects=True
                    )
                    img_response.raise_for_status()

                    filename = image_url.split("/")[-1].split("?")[0]
                    if not filename.lower().endswith(
                        (".jpg", ".jpeg", ".png", ".webp")
                    ):
                        filename += ".jpg"

                    bird.image.save(
                        filename,
                        ContentFile(img_response.content),
                        save=False,
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Could not download image for {b['name']}: {e}"
                        )
                    )

            bird.save()
            created += 1
            self.stdout.write(
                self.style.SUCCESS(f"  Created: {b['name']} ({b['sciName']})")
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nDone. {created} created, {skipped} skipped.")
        )
