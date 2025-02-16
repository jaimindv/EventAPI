from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.permissions import IsAPIKeyAuthenticated, IsRoleAdmin, IsRoleUser

from .models import Event, Ticket
from .serializers import (
    EventSerializer,
    PurchaseTicketSerializer,
    TicketListRetrieveSerializer,
)


class EventViewset(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = "pk"

    def get_permissions(self):
        # Only Admins allowed to create/update/delete event
        if self.action in ["create", "update", "partial_update", "delete"]:
            self.permission_classes = [
                IsAPIKeyAuthenticated,
                IsAuthenticated,
                IsRoleAdmin,
            ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "purchase_tickets":
            self.serializer_class = PurchaseTicketSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
            "message": "Event created successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_data = {
            "message": "Event updated successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @transaction.atomic()
    @action(
        methods=["POST"],
        detail=True,
        url_path="purchase",
        # Only Users are allowed to purchase tickets
        permission_classes=[IsAPIKeyAuthenticated, IsAuthenticated, IsRoleUser],
    )
    def purchase_tickets(self, request, *args, **kwargs):
        user = request.user
        event_id = self.kwargs.get("pk")
        if not Event.objects.filter(id=event_id).exists():
            return Response(
                {
                    "error": "Invalid event.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(
            data=request.data, context={"event_id": event_id}
        )
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data.get("quantity")
        # Create Ticket instance
        ticket_instance = Ticket.objects.create(
            user=user, event_id=event_id, quantity=quantity
        )

        # Update sold tickets in Event
        event_instance = ticket_instance.event
        event_instance.tickets_sold += quantity
        event_instance.save()

        response = {
            "message": "Ticket booked successfully.",
            "data": TicketListRetrieveSerializer(ticket_instance).data,
        }
        return Response(response, status=status.HTTP_201_CREATED)
