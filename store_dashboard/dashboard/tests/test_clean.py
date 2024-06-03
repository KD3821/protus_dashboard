import pytest


def test_clean_store(fake_store, fake_items, test_client):
    store_id = fake_store.get("store_id")
    url = f"/stores/{store_id}"
    url_clean = f"/stores/{store_id}/clean"

    check_res = test_client.get(url)
    assert check_res.status_code == 200

    items = check_res.data.get('store').get('report')
    for fake_item in fake_items:
        for item in items:
            if item.get("item_id") == fake_item.get("item_id"):
                assert item.get("quantity") == fake_item.get("quantity")
                break

    clean_res = test_client.post(url_clean)
    assert clean_res.status_code == 200

    clean_items = clean_res.data.get('store').get('report')
    assert clean_items == []
