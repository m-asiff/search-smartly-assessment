import pytest
from django.core.validators import ValidationError
from decimal import Decimal
from app.models import (
    Category,
    Poi,
)


@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(name="Nature")
    assert Category.objects.count() == 1
    assert category.name == "Nature"


@pytest.mark.django_db
def test_category_unique_name():
    Category.objects.create(name="Adventure")
    with pytest.raises(ValidationError):
        category = Category(name="Adventure")
        category.full_clean()


@pytest.mark.django_db
def test_create_poi():
    category = Category.objects.create(name="Historical")
    poi = Poi.objects.create(
        name="Ancient Ruins",
        external_id=12345,
        category=category,
        avg_rating=Decimal("4.5"),
    )
    assert Poi.objects.count() == 1
    assert poi.name == "Ancient Ruins"
    assert poi.category == category
    assert poi.avg_rating == Decimal("4.5")


@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name="Art")
    assert str(category) == "Art"


@pytest.mark.django_db
def test_poi_str():
    category = Category.objects.create(name="Art")
    poi = Poi.objects.create(
        name="Museum of Modern Art",
        external_id=67890,
        category=category,
        avg_rating=Decimal("4.7"),
    )
    assert str(poi) == "Museum of Modern Art"
