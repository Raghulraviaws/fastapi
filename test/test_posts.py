import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')

    def validate(post):
        return schemas.PostOut(**post)
    
    post_map = map(validate,res.json())
    post_list = list(post_map)

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 200
    
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_one_post_non_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/420")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Posts.id == test_posts[0].id
    assert post.Posts.title == test_posts[0].title
    assert post.Posts.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [("first title", "first content", True),
                                                      ("Second title", "Second content", False),
                                                      ("Last test post", "This is the content", True)])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json = {"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json = {"title":"some title", "content": "some content", "published": True})

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_posts):
    res = authorized_client.delete("/posts/420")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[0].id}", 
                                json = {"title": "update title", "content": "updated content", "id": test_posts[0].id})
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == test_posts[0].title


def test_update_other_user_post(authorized_client, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[3].id}", 
                                json = {"title": "update title", "content": "updated content", "id": test_posts[3].id})
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_posts):
    res = authorized_client.put(f"/posts/420", 
                                json = {"title": "update title", "content": "updated content", "id": 420})
    
    assert res.status_code == 404