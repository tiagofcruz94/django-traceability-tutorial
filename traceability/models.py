"""Training models: they assume slaughter on site, which the real plant doesn't do."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.formats import number_format


class Animal(models.Model):
    """A live animal received for slaughter."""

    class Sex(models.TextChoices):
        MALE = "M", "Macho"
        FEMALE = "F", "Fêmea"

    identification_number = models.CharField(
        "n.º de identificação", max_length=14, unique=True
    )
    sex = models.CharField("sexo", max_length=1, choices=Sex.choices)
    breed = models.CharField("raça", max_length=50)
    birth_date = models.DateField("data de nascimento")
    received_at = models.DateTimeField("data de receção")
    live_weight = models.DecimalField("peso vivo (kg)", max_digits=6, decimal_places=1)

    class Meta:
        verbose_name_plural = "animais"

    def __str__(self):
        return self.identification_number


class DeboningLot(models.Model):
    """A group of carcasses deboned together."""

    lot_number = models.CharField("n.º de lote", max_length=20, unique=True)
    created_at = models.DateTimeField("data de criação", auto_now_add=True)

    class Meta:
        verbose_name = "lote de desmancha"
        verbose_name_plural = "lotes de desmancha"

    def __str__(self):
        return self.lot_number

    def total_hot_weight(self):
        """Sum of the carcasses' hot weight, in kg."""
        # aggregate() returns None for a lot with no carcasses, hence the fallback to 0.
        return self.carcasses.aggregate(total=Sum("hot_weight"))["total"] or Decimal(
            "0"
        )


class Carcass(models.Model):
    """The carcass of one slaughtered animal."""

    # Training values; confirm the real yield range with the factory.
    MIN_YIELD = Decimal("45")
    MAX_YIELD = Decimal("70")

    animal = models.OneToOneField(
        Animal,
        on_delete=models.PROTECT,
        related_name="carcass",
        verbose_name="animal",
    )
    slaughter_number = models.CharField("n.º de abate", max_length=20, unique=True)
    slaughtered_at = models.DateTimeField("data de abate")
    hot_weight = models.DecimalField(
        "peso a quente (kg)", max_digits=6, decimal_places=1
    )

    # Optional: a carcass is weighed before it is assigned to a deboning lot.
    lot = models.ForeignKey(
        DeboningLot,
        on_delete=models.PROTECT,
        related_name="carcasses",
        verbose_name="lote de desmancha",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "carcaça"
        verbose_name_plural = "carcaças"

    def __str__(self):
        return f"{self.slaughter_number} ({self.animal})"

    def carcass_yield(self):
        """Hot weight as a percentage of live weight, or None if there is no live weight."""
        if self.animal.live_weight:
            return (self.hot_weight / self.animal.live_weight) * 100
        return None

    def clean(self):
        """Reject a yield outside MIN_YIELD–MAX_YIELD: it usually means a weighing error."""
        # Missing fields are reported by their own validation; there's nothing to compare yet.
        if self.animal_id is None or self.hot_weight is None:
            return

        carcass_yield = self.carcass_yield()

        if carcass_yield is None:
            return

        if carcass_yield < self.MIN_YIELD or carcass_yield > self.MAX_YIELD:
            # :.1f always writes a dot; number_format follows the site's language
            raise ValidationError(
                {
                    "hot_weight": f"Rendimento de {number_format(carcass_yield, 1)} % fora do intervalo aceitável ({self.MIN_YIELD}–{self.MAX_YIELD} %). Verifique o peso a quente."
                }
            )
