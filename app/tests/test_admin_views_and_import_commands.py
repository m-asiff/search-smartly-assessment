import io
import xml.etree.ElementTree as ET
from unittest.mock import patch

import pytest
from django.urls import reverse

from app.management.commands.import_data import Command
from app.models import Poi


@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpassword",
    )


@pytest.fixture
def client_logged_in(client, admin_user):
    client.login(username="admin", password="adminpassword")
    return client


def test_admin_panel_access(client_logged_in):
    # Test if admin panel is accessible
    response = client_logged_in.get(reverse("admin:index"))
    assert response.status_code == 200


@pytest.mark.django_db
@patch("app.management.commands.import_data.ET.parse")
def test_process_xml_file(mock_parse):
    xml_content = """
    <root>
        <DATA_RECORD>
            <pid>123</pid>
            <pname>Test Name</pname>
            <pcategory>Test</pcategory>
            <pratings>1,1,3,1,4,1,5,3,1,2</pratings>
        </DATA_RECORD>
    </root>
    """
    xml_file = io.StringIO(xml_content)

    parse_return = mock_parse.return_value

    parse_return.getroot.return_value.findall.return_value = (
        ET.ElementTree(ET.fromstring(xml_content))
        .getroot()
        .findall("DATA_RECORD")
    )
    import_command = Command()

    import_command.process_xml_file(xml_file)
    assert Poi.objects.count() == 1


@pytest.mark.django_db
@patch("builtins.open")
def test_process_json_file(mock_open):
    json = (
        '[{"id":"123","name":"Test","category":"Test","ratings":[2]}]'
    )

    json_file = io.StringIO(json)

    mock_open.return_value.__enter__.return_value.read.return_value = (
        json
    )

    import_command = Command()
    import_command.process_json_file(json_file)

    assert Poi.objects.count() == 1
