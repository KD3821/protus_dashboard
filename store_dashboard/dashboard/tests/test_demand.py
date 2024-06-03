import pytest


@pytest.mark.usefixtures("fake_store")
class TestStoreDemand:
    store_id = "test123"
    operation = "demand"
    quantity = 1
    url = f"/stores/{store_id}"
    url_group = f"/stores/{store_id}/group_op"

    def test_demand_one(self, test_client, fake_item):
        payload = {
            "operation": self.operation,
            "item_id": fake_item.get('item_id'),
            "quantity": self.quantity
        }
        response = test_client.post(self.url, payload, format='json')
        assert response.status_code == 200
        items = response.data.get('store').get('report')
        for item in items:
            if item.get('item_id') == fake_item.get('item_id'):
                new_quantity = item.get('quantity')
                break
        assert new_quantity == fake_item.get("quantity") - self.quantity

    def test_demand_many(self, test_client, fake_items):
        demand_items = list()
        items_counter = len(fake_items)
        items_left = 0

        for fake_item in fake_items:
            demand_items.append({
                "item_id": fake_item.get("item_id"),
                "quantity": self.quantity
            })
            if fake_item.get("quantity") <= self.quantity:
                items_counter -= 1

        payload = {
            "operation": self.operation,
            "items": demand_items
        }
        response = test_client.post(self.url_group, payload, format='json')
        items = response.data.get('store').get('report')

        assert response.status_code == 200
        for fake_item in fake_items:
            for item in items:
                if item.get("item_id") == fake_item.get("item_id"):
                    items_left += 1
                    assert item.get("quantity") == fake_item.get("quantity") - self.quantity
                    break
        assert items_counter == items_left
