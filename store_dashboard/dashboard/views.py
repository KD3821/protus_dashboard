from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import stores_collection
from .serializers import ManyItemSerializer, OneItemSerializer
from .utils import StoreProcessor


@api_view(["GET", "POST"])
def store_one(request, *args, **kwargs):
    store_id = kwargs.get("store_id")
    store = stores_collection.find_one({"store_id": store_id})

    if store is None:
        return Response({"store": None})

    sp = StoreProcessor(store_id)

    if request.method == "POST":
        data = request.data
        serializer = OneItemSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        operation = valid_data.get("operation")

        if operation == "demand":
            sp.demand(valid_data)
        elif operation == "supply":
            sp.supply(valid_data)

    return Response({"store": {"store_id": store_id, "report": sp.get_items()}})


@api_view(["POST"])
def store_group(request, *args, **kwargs):
    store_id = kwargs.get("store_id")
    store = stores_collection.find_one({"store_id": store_id})

    if store is None:
        return Response({"store": None})

    sp = StoreProcessor(store_id)

    data = request.data
    serializer = ManyItemSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    valid_data = serializer.validated_data
    operation = valid_data.get("operation")

    if operation == "demand":
        sp.demand_many(valid_data.get("items"))
    elif operation == "supply":
        sp.supply_many(valid_data.get("items"))

    return Response({"store": {"store_id": store_id, "report": sp.get_items()}})


@api_view(["POST"])
def store_clean(request, *args, **kwargs):
    store_id = kwargs.get("store_id")
    store = stores_collection.find_one({"store_id": store_id})

    if store is None:
        return Response({"store": None})

    sp = StoreProcessor(store_id)
    sp.clean()

    return Response({"store": {"store_id": store_id, "report": sp.get_items()}})


@api_view(["GET"])
def store_xlsx(request, *args, **kwargs):
    store_id = kwargs.get("store_id")
    store = stores_collection.find_one({"store_id": store_id})

    if store is None:
        return Response({"store": None})

    sp = StoreProcessor(store_id)
    file, filename = sp.report_xlsx()

    return FileResponse(file, filename=filename, as_attachment=True)
