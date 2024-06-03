import pytest


@pytest.mark.usefixtures("fake_store")
class TestStoreReport:
    store_id = "test123"
    url = f"/stores/{store_id}"
    url_xlsx = f"/stores/{store_id}/xlsx_report"

    def test_report_one(self, test_client, fake_item):
        response = test_client.get(self.url)
        assert response.status_code == 200
        items = response.data.get('store').get('report')
        assert len(items) == 1
        assert items[0].get("item_id") == fake_item.get("item_id")

    def test_report_many(self, test_client, fake_items):
        items_counter = len(fake_items)
        items_received = 0
        response = test_client.get(self.url)
        assert response.status_code == 200
        items = response.data.get("store").get("report")
        for fake_item in fake_items:
            for item in items:
                if item.get("item_id") == fake_item.get("item_id"):
                    items_received += 1
                    assert item.get("quantity") == fake_item.get("quantity")
                    break
        assert items_counter == items_received
