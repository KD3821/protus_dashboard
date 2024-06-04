"""
run tests with command: pytest --ignore=mongodata/ -vvl
"""

import pytest


@pytest.mark.usefixtures("fake_store")
class TestStoreSupply:
    store_id = "test123"
    operation = "supply"
    quantity = 5
    url = f"/stores/{store_id}"
    url_group = f"/stores/{store_id}/group_op"

    def test_supply_one(self, test_client, fake_item):
        payload = {
            "operation": self.operation,
            "item_id": fake_item.get("item_id"),
            "quantity": self.quantity,
        }
        response = test_client.post(self.url, payload, format="json")
        assert response.status_code == 200

        items = response.data.get("store").get("report")
        for item in items:
            if item.get("item_id") == fake_item.get("item_id"):
                new_quantity = item.get("quantity")
                break
        assert new_quantity == fake_item.get("quantity") + self.quantity

    def test_supply_many(self, test_client, fake_items):
        supply_items = list()
        for fake_item in fake_items:
            supply_items.append(
                {"item_id": fake_item.get("item_id"), "quantity": self.quantity}
            )
        payload = {"operation": self.operation, "items": supply_items}
        response = test_client.post(self.url_group, payload, format="json")
        assert response.status_code == 200

        items = response.data.get("store").get("report")
        for fake_item in fake_items:
            for item in items:
                if item.get("item_id") == fake_item.get("item_id"):
                    assert (
                        item.get("quantity")
                        == fake_item.get("quantity") + self.quantity
                    )
                    break
