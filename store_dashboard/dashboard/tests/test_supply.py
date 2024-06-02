import pytest
from rest_framework import status


@pytest.mark.usefixtures("mongodb", "fake_store")
class TestStoreSupply:

    def test_supply_one(self, test_client):
        url = "/stores/test123"
        payload = {
            "operation": "supply",
            "item_id": "Test_1",
            "quantity": 5
        }
        response = test_client.post(url, payload)
        assert response.status_code == status.HTTP_200_OK
