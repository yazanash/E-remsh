from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from ..customer.firebase_utils import send_fcm_v1_notification


@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    if not created:  # We only care about updates
        # Check the status of the order
        message_title = ""
        message_body = ""

        if instance.status == "PR":
            message_title = "Order In Progress"
            message_body = f"Your order #{instance.id} is now in progress. Stay tuned!"
        elif instance.status == "P":
            message_title = "Order Pending"
            message_body = f"Your order #{instance.id} is pending. We’ll update you soon!"
        elif instance.status == "S":
            message_title = "Order Shipped"
            message_body = f"Your order #{instance.id} has been shipped successfully."
        elif instance.status == "C":
            message_title = "Order Canceled"
            message_body = f"Your order #{instance.id} has been canceled. Contact support for help if needed."

            # Get the user's device token
            user_device_token = instance.user.device_token  # Ensure device tokens are stored in the User model

            # Send the notification
            if user_device_token:
                send_fcm_v1_notification(user_device_token, message_title, message_body)
