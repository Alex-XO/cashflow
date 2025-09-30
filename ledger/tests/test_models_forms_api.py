from datetime import date
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient
from catalog.models import Type, Status, Category, Subcategory
from ledger.models import CashflowRecord
from ledger.forms import CashflowRecordForm


class LedgerModelFormApiTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.t_income = Type.objects.create(name="Пополнение")
        self.t_spend = Type.objects.create(name="Списание")
        self.c_income = Category.objects.create(name="Кат. пополнений", type=self.t_income)
        self.c_spend = Category.objects.create(name="Инфраструктура", type=self.t_spend)
        self.sc_income = Subcategory.objects.create(name="Подкат. пополнений", category=self.c_income)
        self.sc_vps = Subcategory.objects.create(name="VPS", category=self.c_spend)
        self.status_personal = Status.objects.create(name="Личное")

    def test_model_date_validation(self):
        r = CashflowRecord(
            record_date=date(1999, 12, 31),
            status=self.status_personal,
            type=self.t_income,
            category=self.c_income,
            subcategory=self.sc_income,
            amount=Decimal("10.00"),
        )
        with self.assertRaises(ValidationError):
            r.clean()

    def test_model_relations_validation(self):
        r = CashflowRecord(
            record_date=date.today(),
            status=self.status_personal,
            type=self.t_income,
            category=self.c_spend,
            subcategory=self.sc_vps,
            amount=Decimal("1.00"),
        )
        with self.assertRaises(ValidationError):
            r.clean()

    def test_model_amount_positive(self):
        r = CashflowRecord(
            record_date=date.today(),
            status=self.status_personal,
            type=self.t_income,
            category=self.c_income,
            subcategory=self.sc_income,
            amount=Decimal("0"),
        )
        with self.assertRaises(Exception):
            r.full_clean()

    def test_form_limits_and_required(self):
        form = CashflowRecordForm(data={
            "record_date": "1999-01-01",
            "status": self.status_personal.id,
            "type": self.t_income.id,
            "category": self.c_income.id,
            "subcategory": self.sc_income.id,
            "amount": "-1",
            "comment": "x" * 3000,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("record_date", form.errors)
        self.assertIn("amount", form.errors)
        self.assertIn("comment", form.errors)

    def test_form_queryset_narrowing(self):
        form = CashflowRecordForm(data={
            "record_date": date.today().isoformat(),
            "status": self.status_personal.id,
            "type": self.t_income.id,
        })
        qs = list(form.fields["category"].queryset.values_list("id", flat=True))
        self.assertIn(self.c_income.id, qs)
        self.assertNotIn(self.c_spend.id, qs)

    def test_api_create_record_ok(self):
        payload = {
            "record_date": date.today().isoformat(),
            "status": self.status_personal.id,
            "type": self.t_income.id,
            "category": self.c_income.id,
            "subcategory": self.sc_income.id,
            "amount": "123.45",
            "comment": "ok",
        }
        r = self.api.post("/api/records/", payload, format="json")
        self.assertEqual(r.status_code, 201)

    def test_api_create_record_relation_error(self):
        payload = {
            "record_date": date.today().isoformat(),
            "status": self.status_personal.id,
            "type": self.t_income.id,
            "category": self.c_spend.id,
            "subcategory": self.sc_vps.id,
            "amount": "10",
        }
        r = self.api.post("/api/records/", payload, format="json")
        self.assertEqual(r.status_code, 400)