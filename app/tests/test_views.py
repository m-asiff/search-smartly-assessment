import pytest
from django.urls import reverse
from app.models import Category, Poi


@pytest.mark.django_db
def test_poi_list_view_no_filters(client):
    url = reverse("poi_list_view")
    response = client.get(url)
    assert response.status_code == 200
    assert "categories" in response.context


@pytest.mark.django_db
def test_poi_list_view_id_search(client):
    category = Category.objects.create(name="Test Category")
    poi = Poi.objects.create(
        name="Test Poi",
        external_id=123,
        category=category,
        avg_rating=4.5,
    )
    url = reverse("poi_list_view") + "?id_search=" + str(poi.id)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["page_obj"]) == 1
    assert response.context["page_obj"].object_list[0].id == poi.id


@pytest.mark.django_db
def test_poi_list_view_external_id_search(client):
    category = Category.objects.create(name="Test Category")
    poi = Poi.objects.create(
        name="Another Test Poi",
        external_id=456,
        category=category,
        avg_rating=4.0,
    )
    url = (
        reverse("poi_list_view")
        + "?external_id_search="
        + str(poi.external_id)
    )
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["page_obj"]) == 1
    assert (
        response.context["page_obj"].object_list[0].external_id
        == poi.external_id
    )


@pytest.mark.django_db
def test_poi_list_view_filter_query(client):
    category1 = Category.objects.create(name="Category1")
    category2 = Category.objects.create(name="Category2")
    Poi.objects.create(
        name="Poi in Category1",
        external_id=789,
        category=category1,
        avg_rating=3.5,
    )
    Poi.objects.create(
        name="Poi not in query",
        external_id=101,
        category=category2,
        avg_rating=4.2,
    )
    url = reverse("poi_list_view") + "?filter=Category1"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["page_obj"]) == 1
    assert (
        response.context["page_obj"].object_list[0].category.name
        == "Category1"
    )
