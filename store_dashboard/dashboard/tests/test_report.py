"""
run tests with command: pytest --ignore=mongodata/ -vvl
"""

import openpyxl
import pytest


@pytest.mark.usefixtures("fake_store")
class TestStoreReport:
    store_id = "test123"
    url = f"/stores/{store_id}"
    url_xlsx = f"/stores/{store_id}/xlsx_report"

    def test_report_one(self, test_client, fake_item):
        response = test_client.get(self.url)
        assert response.status_code == 200
        items = response.data.get("store").get("report")
        assert len(items) == 1
        assert items[0].get("item_id") == fake_item.get("item_id")

    def test_report_many(self, test_client, fake_items):
        response = test_client.get(self.url)
        assert response.status_code == 200
        items = response.data.get("store").get("report")
        for fake_item in fake_items:
            for item in items:
                if item.get("item_id") == fake_item.get("item_id"):
                    assert item.get("quantity") == fake_item.get("quantity")
                    break
        assert len(fake_items) == len(items)

    def test_report_xlsx(self, fake_items, test_client):
        test_filename = f"STORE_{self.store_id}.xlsx"
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        response = test_client.get(self.url_xlsx)

        assert response.status_code == 200
        assert response.filename == test_filename

        file_repr = b"".join(response.streaming_content).decode()
        assert file_repr == sheet.__repr__()
