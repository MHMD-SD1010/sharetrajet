import json
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from app.trajets.models import FuelPrice


class Command(BaseCommand):
    help = "Charge les prix du carburant depuis un fichier JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file", type=str, help="Chemin vers le fichier JSON contenant les prix"
        )

    def handle(self, *args, **options):
        json_file = options["json_file"]

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            today = timezone.now().date()
            created_count = 0
            updated_count = 0

            for wilaya, prices in data.items():
                # Traiter l'essence
                if "essence" in prices:
                    fuel_price, created = FuelPrice.objects.update_or_create(
                        wilaya=wilaya,
                        fuel_type="ESSENCE",
                        effective_date=today,
                        defaults={"price_per_liter": Decimal(str(prices["essence"]))},
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                # Traiter le diesel
                if "diesel" in prices:
                    fuel_price, created = FuelPrice.objects.update_or_create(
                        wilaya=wilaya,
                        fuel_type="DIESEL",
                        effective_date=today,
                        defaults={"price_per_liter": Decimal(str(prices["diesel"]))},
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Prix du carburant chargés avec succès!\n"
                    f"Créés: {created_count}, Mis à jour: {updated_count}"
                )
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Fichier non trouvé: {json_file}"))
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f"Erreur de format JSON dans: {json_file}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur: {str(e)}"))
