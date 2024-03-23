import pytest
from app import models

@pytest.fixture
def test_vote(session, test_posts, test_user):
    vote = models.Votes(user_id = test_user["id"], post_id = test_posts[3].id)
    session.add(vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409

def test_remove_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 0}
    )
    assert res.status_code == 201


def test_remove_vote_non_exist(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 0}
    )
    assert res.status_code == 404

def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": 420, "dir": 1}
    )
    assert res.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert res.status_code == 401