from django.db import models

from core.custom_auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    total_tickets = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)

    @property
    def available_tickets(self):
        return self.total_tickets - self.tickets_sold

    def __str__(self):
        return f"{self.id} - {self.name}"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ticket")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket")
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
