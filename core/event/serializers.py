from django.utils import timezone
from rest_framework import serializers

from .models import Event, Ticket


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date",
            "total_tickets",
            "tickets_sold",
            "available_tickets",
        ]


class PurchaseTicketSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

    def validate(self, attrs):
        quantity = attrs.get("quantity")
        event_id = self.context.get("event_id")
        event_obj = Event.objects.filter(id=event_id).first()
        if event_obj.available_tickets < quantity:
            raise serializers.ValidationError(
                {
                    "error": (
                        "Not able to purchase tickets as available tickets "
                        f"({event_obj.available_tickets}) are less than the specified "
                        f"quantity ({quantity})."
                    )
                }
            )

        if event_obj.date < timezone.now().date():
            raise serializers.ValidationError(
                {
                    "error": "Caannot purchase the tickets as event has already started or completed."
                }
            )
        return attrs


class TicketListRetrieveSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "event",
            "quantity",
            "purchase_date",
        ]
