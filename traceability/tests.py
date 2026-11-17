from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Animal, Carcass, DeboningLot


class LoggedInTestCase(TestCase):
    """Base class for tests that need a logged-in user."""

    def setUp(self):
        self.user = User.objects.create_user(username="operador", password="segredo123")
        self.client.force_login(self.user)


class DeboningLotTests(TestCase):
    """Tests for DeboningLot.total_hot_weight()."""

    def test_total_hot_weight_empty_lot_is_zero(self):
        lot = DeboningLot.objects.create(lot_number="T001")

        self.assertEqual(lot.total_hot_weight(), Decimal("0"))

    def test_total_hot_weight_sums_carcasses(self):
        lot = DeboningLot.objects.create(lot_number="T002")

        animal1 = Animal.objects.create(
            identification_number="PT0001",
            sex=Animal.Sex.MALE,
            breed="Barrosã",
            birth_date=date(2026, 10, 1),
            received_at=timezone.now(),
            live_weight=Decimal("600.0"),
        )

        animal2 = Animal.objects.create(
            identification_number="PT0002",
            sex=Animal.Sex.FEMALE,
            breed="Barrosã",
            birth_date=date(2026, 10, 5),
            received_at=timezone.now(),
            live_weight=Decimal("500.0"),
        )

        Carcass.objects.create(
            animal=animal1,
            lot=lot,
            slaughter_number="34534",
            slaughtered_at=timezone.now(),
            hot_weight=Decimal("200.0"),
        )

        Carcass.objects.create(
            animal=animal2,
            lot=lot,
            slaughter_number="34536",
            slaughtered_at=timezone.now(),
            hot_weight=Decimal("180.5"),
        )

        self.assertEqual(lot.total_hot_weight(), Decimal("380.5"))


class LotViewTests(LoggedInTestCase):
    """Tests for the lot list and lot detail pages."""

    def setUp(self):
        super().setUp()
        # Two carcasses (200.0 + 180.5), so the total 380.5 can't be mistaken for either weight.
        self.lot = DeboningLot.objects.create(lot_number="T100")

        animal = Animal.objects.create(
            identification_number="PT0001",
            sex=Animal.Sex.MALE,
            breed="Barrosã",
            birth_date=date(2026, 10, 1),
            received_at=timezone.now(),
            live_weight=Decimal("600.0"),
        )

        animal2 = Animal.objects.create(
            identification_number="PT0002",
            sex=Animal.Sex.MALE,
            breed="Barrosã",
            birth_date=date(2026, 10, 1),
            received_at=timezone.now(),
            live_weight=Decimal("600.0"),
        )

        Carcass.objects.create(
            animal=animal,
            lot=self.lot,
            slaughter_number="34534",
            slaughtered_at=timezone.now(),
            hot_weight=Decimal("200.0"),
        )

        Carcass.objects.create(
            animal=animal2,
            lot=self.lot,
            slaughter_number="34535",
            slaughtered_at=timezone.now(),
            hot_weight=Decimal("180.5"),
        )

    def test_page_loads(self):
        response = self.client.get(reverse("traceability:lot_list"))

        self.assertEqual(response.status_code, 200)

    def test_shows_lot_number_and_total(self):
        response = self.client.get(reverse("traceability:lot_list"))

        self.assertContains(response, "T100")
        self.assertContains(response, "380,5")

    def test_list_links_to_lot_detail(self):
        response = self.client.get(reverse("traceability:lot_list"))

        url = reverse("traceability:lot_detail", args=[self.lot.pk])
        self.assertContains(response, url)

    def test_detail_shows_lot_and_total(self):
        url = reverse("traceability:lot_detail", args=[self.lot.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "T100")
        self.assertContains(response, "380,5")

    def test_detail_unknown_lot_returns_404(self):
        # self.lot is the only lot; pk + 1 (not a fixed number) because ids aren't reset in PostgreSQL.
        url = reverse("traceability:lot_detail", args=[self.lot.pk + 1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_detail_empty_lot_hides_total(self):
        empty_lot = DeboningLot.objects.create(lot_number="T002")

        url = reverse("traceability:lot_detail", args=[empty_lot.pk])
        response = self.client.get(url)

        self.assertNotContains(response, "Peso total")


class CarcassValidationTests(TestCase):
    """Tests for the yield check in Carcass.clean() (animal with 600 kg live weight)."""

    def setUp(self):
        self.animal = Animal.objects.create(
            identification_number="PT0001",
            sex=Animal.Sex.MALE,
            breed="Barrosã",
            birth_date=date(2024, 3, 1),
            received_at=timezone.now(),
            live_weight=Decimal("600.0"),
        )

    def test_impossible_yield_is_rejected(self):
        carcass = Carcass(
            animal=self.animal,
            slaughter_number="50001",
            slaughtered_at=timezone.now(),
            hot_weight=Decimal("165.0"),  # 27.5 % of 600 kg
        )

        with self.assertRaises(ValidationError):
            carcass.full_clean()

    def test_normal_yield_is_accepted(self):
        carcass2 = Carcass(
            animal=self.animal,
            slaughter_number="50002",
            slaughtered_at=timezone.now(),
            hot_weight=Decimal("330.0"),  # 55 % of 600 kg
        )
        # No assert needed: full_clean() raises ValidationError if the yield is rejected.
        carcass2.full_clean()

    def test_carcass_yield_is_calculated(self):
        carcass3 = Carcass(
            animal=self.animal,
            slaughter_number="50003",
            slaughtered_at=timezone.now(),
            hot_weight=Decimal("330.0"),  # 55 % of 600 kg
        )
        self.assertEqual(carcass3.carcass_yield(), Decimal("55.0"))


class CarcassCreateViewTests(LoggedInTestCase):
    """Tests for the carcass_create view where new carcasses are added."""

    def setUp(self):
        super().setUp()
        self.animal = Animal.objects.create(
            identification_number="PT0001",
            sex=Animal.Sex.MALE,
            breed="Barrosã",
            birth_date=date(2024, 3, 1),
            received_at=timezone.now(),
            live_weight=Decimal("600.0"),
        )
        self.url = reverse("traceability:carcass_create")

    def valid_data(self):
        """Form data for a carcass with a 55 % yield."""
        return {
            "animal": self.animal.pk,
            "slaughter_number": "50001",
            "slaughtered_at": "2026-11-16 10:00",
            "hot_weight": "330.0",
        }

    def test_valid_post_creates_carcass_and_redirects(self):
        response = self.client.post(self.url, self.valid_data())

        self.assertRedirects(response, reverse("traceability:lot_list"))
        self.assertEqual(Carcass.objects.count(), 1)

    def test_valid_post_shows_success_message(self):
        response = self.client.post(self.url, self.valid_data(), follow=True)

        self.assertContains(response, "Carcaça 50001 adicionada.")

    def test_impossible_yield_is_rejected(self):
        data = self.valid_data()
        data["hot_weight"] = "165.0"  # 27.5 % of 600 kg

        response = self.client.post(self.url, data)

        self.assertEqual(Carcass.objects.count(), 0)
        self.assertContains(response, "fora do intervalo aceitável")
        self.assertContains(response, "27,5")

    def test_comma_decimal_is_accepted(self):
        data = self.valid_data()
        # Portuguese users type decimals with a comma, not a dot.
        data["hot_weight"] = "330,0"

        response = self.client.post(self.url, data)

        self.assertRedirects(response, reverse("traceability:lot_list"))
        self.assertEqual(Carcass.objects.count(), 1)


class HomeRedirectTests(LoggedInTestCase):
    """Tests for the redirect from the root address to the lot list view."""

    def test_root_redirects_to_lot_list(self):
        url = "/"
        response = self.client.get(url)

        self.assertRedirects(response, reverse("traceability:lot_list"))
