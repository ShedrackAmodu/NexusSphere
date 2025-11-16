from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Item
from rest_framework.test import APIClient
from rest_framework import status


class HomepageTests(TestCase):
    def test_homepage_status_and_content(self):
        """GET / should return 200 and include project name text."""
        resp = self.client.get(reverse("core:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "NexusSphere")


class ItemCRUDTests(TestCase):
    def setUp(self):
        # create two users and a sample item owned by `user`
        self.user = User.objects.create_user(username="owner", password="pass")
        self.other = User.objects.create_user(username="other", password="pass")
        self.item = Item.objects.create(name="Test Item", description="Desc", owner=self.user)

    def test_item_list(self):
        resp = self.client.get(reverse("core:item_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test Item")

    def test_item_detail(self):
        resp = self.client.get(reverse("core:item_detail", args=[self.item.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Desc")

    def test_item_create(self):
        # must be logged in to create; owner should be set automatically
        self.client.login(username="owner", password="pass")
        resp = self.client.post(reverse("core:item_create"), {"name": "New Item", "description": "New"})
        # should redirect to list
        self.assertEqual(resp.status_code, 302)
        new = Item.objects.get(name="New Item")
        self.assertEqual(new.owner, self.user)

    def test_item_update(self):
        # must be logged in as owner to update
        self.client.login(username="owner", password="pass")
        resp = self.client.post(reverse("core:item_update", args=[self.item.pk]), {"name": "Updated", "description": "X"})
        self.assertEqual(resp.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated")

    def test_item_update_forbidden_for_non_owner(self):
        # other authenticated user cannot update (403)
        self.client.login(username="other", password="pass")
        resp = self.client.post(reverse("core:item_update", args=[self.item.pk]), {"name": "Hacked", "description": "X"})
        self.assertEqual(resp.status_code, 403)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Test Item")

    def test_item_delete(self):
        # must be logged in as owner to delete
        self.client.login(username="owner", password="pass")
        resp = self.client.post(reverse("core:item_delete", args=[self.item.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())

    def test_item_delete_forbidden_for_non_owner(self):
        # other authenticated user cannot delete (403)
        # recreate item for this test
        item2 = Item.objects.create(name="ToDelete", description="X", owner=self.user)
        self.client.login(username="other", password="pass")
        resp = self.client.post(reverse("core:item_delete", args=[item2.pk]))
        self.assertEqual(resp.status_code, 403)
        self.assertTrue(Item.objects.filter(pk=item2.pk).exists())


class ItemAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="pass")
        self.other = User.objects.create_user(username="apiother", password="pass")
        self.item = Item.objects.create(name="API Item", description="X", owner=self.user)
        self.client = APIClient()

    def test_api_list(self):
        resp = self.client.get("/api/items/")
        self.assertEqual(resp.status_code, 200)

    def test_api_create_requires_auth(self):
        resp = self.client.post("/api/items/", {"name": "New API", "description": "D"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_create_authenticated(self):
        self.client.login(username="apiuser", password="pass")
        resp = self.client.post("/api/items/", {"name": "New API", "description": "D"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["owner"], "apiuser")

    def test_api_update_forbidden_for_non_owner(self):
        self.client.login(username="apiother", password="pass")
        resp = self.client.patch(f"/api/items/{self.item.pk}/", {"name": "X"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

from django.test import TestCase

# Create your tests here.
