"""
run tests with command: pytest --ignore=mongodata/ -vvl
"""

import asyncio
import json

import pytest
from channels.testing import WebsocketCommunicator


@pytest.mark.usefixtures("fake_store")
class TestStoreWebsockets:
    store_id = "test123"
    url = f"ws/stores/{store_id}"
    url_one = f"/stores/{store_id}"
    url_many = f"/stores/{store_id}/group_op"
    url_clean = f"/stores/{store_id}/clean"
    supply_operation = "supply"
    supply_quantity = 5
    demand_operation = "demand"
    demand_quantity = 1

    @pytest.mark.asyncio
    async def test_supply_one(self, asgi_app, test_client, fake_item):
        communicator = WebsocketCommunicator(asgi_app, self.url)
        connected, _ = await communicator.connect()
        assert connected
        payload = {
            "operation": self.supply_operation,
            "item_id": fake_item.get("item_id"),
            "quantity": self.supply_quantity,
        }
        supply_res = await asyncio.to_thread(
            test_client.post, self.url_one, payload, format="json"
        )
        assert supply_res.status_code == 200

        response = await communicator.receive_from()
        assert response == json.dumps(
            {
                "store": {
                    "store_id": self.store_id,
                    "report": [
                        {
                            "item_id": fake_item.get("item_id"),
                            "quantity": fake_item.get("quantity")
                            + self.supply_quantity,
                        }
                    ],
                }
            }
        )
        await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_supply_many(self, asgi_app, test_client, fake_items):
        communicator = WebsocketCommunicator(asgi_app, self.url)
        connected, _ = await communicator.connect()
        assert connected

        supply_items = list()
        for fake_item in fake_items:
            supply_items.append(
                {"item_id": fake_item.get("item_id"), "quantity": self.supply_quantity}
            )
        payload = {"operation": self.supply_operation, "items": supply_items}
        supply_res = await asyncio.to_thread(
            test_client.post, self.url_many, payload, format="json"
        )
        assert supply_res.status_code == 200

        items = list()
        for fake_item in fake_items:
            items.append(
                {
                    "item_id": fake_item.get("item_id"),
                    "quantity": fake_item.get("quantity") + self.supply_quantity,
                }
            )

        response = await communicator.receive_from()
        assert response == json.dumps(
            {"store": {"store_id": self.store_id, "report": items}}
        )
        await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_demand_one(self, asgi_app, test_client, fake_item):
        communicator = WebsocketCommunicator(asgi_app, self.url)
        connected, _ = await communicator.connect()
        assert connected
        payload = {
            "operation": self.demand_operation,
            "item_id": fake_item.get("item_id"),
            "quantity": self.demand_quantity,
        }
        demand_res = await asyncio.to_thread(
            test_client.post, self.url_one, payload, format="json"
        )
        assert demand_res.status_code == 200

        response = await communicator.receive_from()
        assert response == json.dumps(
            {
                "store": {
                    "store_id": self.store_id,
                    "report": [
                        {
                            "item_id": fake_item.get("item_id"),
                            "quantity": fake_item.get("quantity")
                            - self.demand_quantity,
                        }
                    ],
                }
            }
        )
        await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_demand_many(self, asgi_app, test_client, fake_items):
        communicator = WebsocketCommunicator(asgi_app, self.url)
        connected, _ = await communicator.connect()
        assert connected

        demand_items = list()
        for fake_item in fake_items:
            demand_items.append(
                {"item_id": fake_item.get("item_id"), "quantity": self.demand_quantity}
            )
        payload = {"operation": self.demand_operation, "items": demand_items}
        demand_res = await asyncio.to_thread(
            test_client.post, self.url_many, payload, format="json"
        )
        assert demand_res.status_code == 200

        items = list()
        for fake_item in fake_items:
            if fake_item.get("quantity") > self.demand_quantity:
                items.append(
                    {
                        "item_id": fake_item.get("item_id"),
                        "quantity": fake_item.get("quantity") - self.demand_quantity,
                    }
                )

        response = await communicator.receive_from()
        assert response == json.dumps(
            {"store": {"store_id": self.store_id, "report": items}}
        )
        await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_clean_store(self, asgi_app, test_client, fake_items):
        communicator = WebsocketCommunicator(asgi_app, self.url)
        connected, _ = await communicator.connect()
        assert connected

        clean_res = await asyncio.to_thread(test_client.post, self.url_clean)
        assert clean_res.status_code == 200

        response = await communicator.receive_from()
        assert response == json.dumps(
            {"store": {"store_id": self.store_id, "report": []}}
        )
        await communicator.disconnect()
