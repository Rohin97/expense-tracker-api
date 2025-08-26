import pytest
import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_token_create_list():
    client = APIClient()

    # register
    r = client.post("/auth/register/", {"username":"daven","password":"soccergirl"}, format="json")
    assert r.status_code in (200,201)

    # token
    r = client.post("/auth/token/", {"username":"daven","password":"soccergirl"}, format="json")
    assert r.status_code == 200
    access = r.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    # create expense
    r = client.post("/api/expenses/", {"description":"Coffee","category":"Food & supplies","amount":"3.50"}, format="json")
    assert r.status_code in (200,201)

    # list (should be 1)
    r = client.get("/api/expenses/")
    data = json.loads(r.content)
    assert r.status_code == 200
    assert len(data) == 1

@pytest.mark.django_db
def test_user_is_readonly_on_update():
    from expenses.models import Expense
    u1 = User.objects.create_user(username="daven", password="soccergirl")
    u2 = User.objects.create_user(username="shelby", password="soccergirl")

    client = APIClient()
    # token for u1
    tok = client.post("/auth/token/", {"username":"daven","password":"soccergirl"}, format="json").data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {tok}")

    # create
    r = client.post("/api/expenses/", {"description":"Movie snacks","category":"Entertainment","amount":"21.99"}, format="json")
    data = json.loads(r.content)
    exp_id = data["id"]
    print(exp_id)

    # attempt to change owner (should be ignored/forbidden by read_only + perform_update)
    r = client.patch(f"/api/expenses/{exp_id}/", {"user": u2.id}, format="json")
    assert r.status_code == 200
    # confirm ownership unchanged
    r = client.get(f"/api/expenses/{exp_id}/")
    data = json.loads(r.content)
    assert data["user"] == u1.id
