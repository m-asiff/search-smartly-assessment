import pytest
from django.core.management import call_command
from app.models import Poi


@pytest.mark.django_db
def test_import_xml_file():
    call_command("import_data", "app/tests/data/pois_test.xml")
    assert Poi.objects.count() == 3
    poi = Poi.objects.first()
    assert poi.name == "Дзіцячы сад №34"
    assert poi.category.name == "kindergarten"


@pytest.mark.django_db
def test_import_json_file():
    call_command("import_data", "app/tests/data/pois_test.json")
    assert Poi.objects.count() == 3
    poi = Poi.objects.first()
    assert poi.name == "unser Laden, Familie Lackinger"
    assert poi.category.name == "convenience-store"


@pytest.mark.django_db
def test_import_csv_file():
    call_command("import_data", "app/tests/data/pois_test.csv")
    assert Poi.objects.count() == 8
    poi = Poi.objects.first()
    assert poi.name == "ちぬまん"
    assert poi.category.name == "restaurant"
