from rest_framework import serializers


def operation_validation(operation):
    if operation not in ("supply", "demand"):
        raise serializers.ValidationError(
            'Only "supply" & "demand" operations are allowed.'
        )
    return operation


class ItemSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    quantity = serializers.IntegerField()

    def validate(self, data):
        quantity = data.get("quantity")
        if not isinstance(quantity, int):
            raise serializers.ValidationError("Item quantity must be a integer.")
        return data


class OneItemSerializer(ItemSerializer):
    operation = serializers.CharField(validators=[operation_validation])


class ManyItemSerializer(serializers.Serializer):
    operation = serializers.CharField(validators=[operation_validation])
    items = ItemSerializer(many=True, write_only=True)
