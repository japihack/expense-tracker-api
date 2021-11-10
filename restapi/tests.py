from django.test import TestCase
from . import models
from django.urls import reverse
#from unittest import TestCase

# Create your tests here.

#def two_integers_sum(a, b):
#    return a + b

#class TestSum(TestCase):
#    def test_sum(self):
#        self.assertEqual(two_integers_sum(1, 2), 3)


class TestModels(TestCase):
    def test_expense(self):
        expense=models.Expense.objects.create(amount=249.99, merchant="amazon", description="anc headphones", category="music")
        inserted_expense=models.Expense.objects.get(pk=expense.id)

        self.assertEqual(249.99, inserted_expense.amount)
        self.assertEqual("amazon", inserted_expense.merchant)
        self.assertEqual("anc headphones", inserted_expense.description)
        self.assertEqual("music", inserted_expense.category)


class TestViews(TestCase):
    def test_expense_create(self):
        """
        payload = {
            "amount": 50,
            "merchant": "AT&T",
            "description": "cell phone subscription",
            "category": "utilities"
        }

        res = self.client.post(reverse("restapi:expense-list-create"), payload, format="json")

        self.assertEqual(201, res.status_code)

        json_res = res.json()

        # en el test anterior daba un error porque esperaba un string en el amount, por eso lo pasamos como un str
        self.assertEqual(str(payload["amount"]), json_res["amount"])
        self.assertEqual(payload["merchant"], json_res["merchant"])
        self.assertEqual(payload["description"], json_res["description"])
        self.assertEqual(payload["category"], json_res["category"])
        self.assertIsInstance(json_res["id"], int)
        """

        # con serializers:
        payload = {
            "amount": 50.0,
            "merchant": "AT&T",
            "description": "cell phone subscription",
            "category": "utilities"
        }

        res = self.client.post(reverse("restapi:expense-list-create"), payload, format="json")

        self.assertEqual(201, res.status_code)

        json_res = res.json()

        self.assertEqual(payload["amount"], json_res["amount"])
        self.assertEqual(payload["merchant"], json_res["merchant"])
        self.assertEqual(payload["description"], json_res["description"])
        self.assertEqual(payload["category"], json_res["category"])
        self.assertIsInstance(json_res["id"], int)

    def test_expense_list(self):
        res = self.client.get(reverse("restapi:expense-list-create"), format="json")

        self.assertEqual(200, res.status_code)

        json_res = res.json()

        self.assertIsInstance(json_res, list)

        expenses = models.Expense.objects.all()
        self.assertEqual(len(expenses), len(json_res))

    def test_expense_create_required_fields_missing(self):
        payload = {
            "merchant": "AT&T",
            "description": "cell phone subscription",
            "category": "utilities"
        }

        res = self.client.post(reverse("restapi:expense-list-create"), payload, format="json")

        self.assertEqual(400, res.status_code)