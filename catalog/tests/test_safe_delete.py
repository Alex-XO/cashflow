from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from catalog.models import Type, Category, Status, Subcategory
from ledger.models import CashflowRecord
from datetime import date
from decimal import Decimal


class SafeDeleteViewsTests(TestCase):
    def setUp(self):
        self.t = Type.objects.create(name="Списание")
        self.c = Category.objects.create(name="Инфраструктура", type=self.t)
        self.sc = Subcategory.objects.create(name="VPS", category=self.c)
        self.s = Status.objects.create(name="Личное")
        CashflowRecord.objects.create(
            record_date=date.today(),
            status=self.s,
            type=self.t,
            category=self.c,
            subcategory=self.sc,
            amount=Decimal("1.00"),
        )

    def test_delete_type_protected_message(self):
        url = reverse("type_delete", args=[self.t.id])
        r = self.client.post(url, follow=True)
        self.assertEqual(r.status_code, 200)
        msgs = [m.message for m in get_messages(r.wsgi_request)]
        self.assertTrue(any("Невозможно удалить" in m for m in msgs))