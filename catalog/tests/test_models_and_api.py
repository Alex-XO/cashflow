from django.test import TestCase
from rest_framework.test import APIClient
from catalog.models import Type, Status, Category, Subcategory


class CatalogModelApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.t_income = Type.objects.create(name="Пополнение")
        self.t_spend = Type.objects.create(name="Списание")
        self.c_inf = Category.objects.create(name="Инфраструктура", type=self.t_spend)
        self.c_marketing = Category.objects.create(name="Маркетинг", type=self.t_spend)
        self.sc_vps = Subcategory.objects.create(name="VPS", category=self.c_inf)

    def test_unique_category_within_type(self):
        Category.objects.create(name="Уник", type=self.t_income)
        with self.assertRaises(Exception):
            Category.objects.create(name="Маркетинг", type=self.t_spend)

    def test_unique_subcategory_within_category(self):
        with self.assertRaises(Exception):
            Subcategory.objects.create(name="VPS", category=self.c_inf)

    def test_api_categories_filtered_by_type(self):
        r = self.client.get("/api/categories/", {"type": self.t_spend.id})
        self.assertEqual(r.status_code, 200)
        names = {x["name"] for x in (r.json()["results"] if "results" in r.json() else r.json())}
        self.assertIn("Инфраструктура", names)
        self.assertIn("Маркетинг", names)

        r2 = self.client.get("/api/categories/", {"type": self.t_income.id})
        names2 = {x["name"] for x in (r2.json()["results"] if "results" in r2.json() else r2.json())}
        self.assertNotIn("Инфраструктура", names2)

    def test_api_subcategories_filtered_by_category(self):
        r = self.client.get("/api/subcategories/", {"category": self.c_inf.id})
        self.assertEqual(r.status_code, 200)
        names = {x["name"] for x in (r.json()["results"] if "results" in r.json() else r.json())}
        self.assertIn("VPS", names)

    def test_api_quick_add_validations(self):
        # Пустое имя
        bad = self.client.post("/api/types/", {"name": ""}, format="json")
        self.assertEqual(bad.status_code, 400)

        # Дубликат типа
        dup = self.client.post("/api/types/", {"name": "Списание"}, format="json")
        self.assertEqual(dup.status_code, 400)

        # Категория без типа
        bad_cat = self.client.post("/api/categories/", {"name": "X"}, format="json")
        self.assertEqual(bad_cat.status_code, 400)