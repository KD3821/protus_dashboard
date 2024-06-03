import pytest


@pytest.mark.usefixtures("fake_store")
class TestStoreSupply:
    store_id = "test123"
    operation = "supply"
    quantity = 5
    url = f"/stores/{store_id}"
    url_group = f"/stores/{store_id}/group_op"

    def get_item_quantity(self, test_client):
        response = test_client.get(self.url)
        assert response.status_code == 200
        items = response.data.get('store').get('report')
        for item in items:
            if item.get('item_id') == self.item.get('item_id'):
                return item.get('quantity')
        else:
            return None

    def get_quantities(self, test_client):
        quantities = dict()
        response = test_client.get(self.url)
        assert response.status_code == 200
        items = response.data.get('store').get('report')
        for item in items:
            for test_item in self.items:
                if item.get('item_id') == test_item.get('item_id'):
                    quantities[item.get('item_id')] = item.get('quantity')
        return quantities

    def clean_item(self, test_client):
        quantity = self.get_item_quantity(test_client)
        if quantity is not None:
            payload = {
                "operation": "demand",
                "item_id": self.item.get('item_id'),
                "quantity": quantity
            }
            response = test_client.post(self.url, payload, format='json')
            assert response.status_code == 200
        assert self.get_item_quantity(test_client) == None  # noqa

    def test_supply_one(self, test_client, fake_item):
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
        assert new_quantity == fake_item.get("quantity") + self.quantity

    def test_supply_many(self, test_client, fake_items):
        supply_items = list()
        for fake_item in fake_items:
            supply_items.append({
                "item_id": fake_item.get("item_id"),
                "quantity": self.quantity
            })
        payload = {
            "operation": self.operation,
            "items": supply_items
        }
        response = test_client.post(self.url_group, payload, format='json')
        items = response.data.get('store').get('report')
        assert response.status_code == 200
        for fake_item in fake_items:
            for item in items:
                if item.get("item_id") == fake_item.get("item_id"):
                    assert item.get("quantity") == fake_item.get("quantity") + self.quantity
                    break

    # def not_supply_many(self, test_client):
    #     old_quantities = self.get_quantities(test_client)
    #     payload = {
    #         "operation": "supply",
    #         "items": self.items
    #     }
    #     response = test_client.post(self.url_group, payload, format='json')
    #     assert response.status_code == status.HTTP_200_OK
    #     items = response.data.get('store').get('report')
    #     for test_item in self.items:
    #         if (old_q := old_quantities.get(test_item.get('item_id'))) is not None:
    #             for item in items:
    #                 if item.get('item_id') == test_item.get('item_id'):
    #                     assert item.get('quantity') == old_q + test_item.get('quantity')
    #         else:
    #             for item in items:
    #                 if item.get('item_id') == test_item.get('item_id'):
    #                     assert item.get('quantity') == test_item.get('quantity')
