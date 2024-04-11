# models/payment_model.py
from datetime import datetime

class PaymentModel:
    def __init__(self, payment_id, booking_id, customer_number,payment_date=None, duration_minutes = 0, amount=0, is_paid = False, payment_type='mpesa'):
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.customer_number=customer_number
        self.payment_date = payment_date  # Initially set to None
        self.duration_minutes = duration_minutes
        self.amount = amount
        self.is_paid = is_paid  # Initially set to False
        self.payment_type = payment_type  # Default payment type is 'mpesa'

    def calculate_amount(self, duration_minutes, rate_per_minute=0.8):
        return duration_minutes * rate_per_minute

    def make_payment(self):
        # Implement your payment logic here
        # This could involve interacting with a payment gateway or updating a database
        self.is_paid = True  # Mark the payment as paid
        self.payment_date = datetime.now()  # Set payment_date to the current time when payment is made

    def get_payment_details(self):
        # Return payment details as a dictionary
        return {
            'payment_id': self.payment_id,
            'booking_id': self.booking_id,
            'customer_number': self.customer_number,
            'payment_date': self.payment_date,
            "duration_minutes" : self.duration_minutes,
            'amount': self.amount,
            'is_paid': self.is_paid,
            'payment_type': self.payment_type
            # Add other relevant details
        }
