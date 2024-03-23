import pytest
from app import schemas
from jose import jwt

from app.config import settings

def test_create_user(client):
    res = client.post('/users/', json={"email": "test123@gmail.com", "password": "testpass"})

    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "test123@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post('/login', data={"username": test_user["email"], 
                                      "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]

@pytest.mark.parametrize("email, password, status_code", [("wrongemail@gmail.com","wrongpasword",403),
                                                          ('sanjeev@gmail.com', 'wrongpassword', 403),
                                                        ('wrongemail@gmail.com', 'wrongpassword', 403),
                                                        (None, 'password123', 422),
                                                        ('sanjeev@gmail.com', None, 422)])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data = {"username": email, "password": password})
    assert res.status_code == status_code


