import os
import africastalking

class SMSService:
    def __init__(self):
        self.username = os.environ.get('AFRICASTALKING_USERNAME', 'sandbox')
        self.api_key = os.environ.get('AFRICASTALKING_API_KEY')
        if self.api_key:
            africastalking.initialize(self.username, self.api_key)
            self.sms = africastalking.SMS
        else:
            print("Warning: Africa's Talking API key missing")
            self.sms = None

    def send_sms(self, to_number, message_body):
        if not self.sms:
            print("SMS not sent: service not initialized")
            return False
        if not to_number or not message_body:
            return False
        # Ensure number starts with '+' and is in international format
        if not to_number.startswith('+'):
            to_number = '+' + to_number
        try:
            response = self.sms.send(message_body, [to_number])
            print(f"SMS sent to {to_number}: {response}")
            return True
        except Exception as e:
            print(f"Africa's Talking error: {e}")
            return False

sms_service = SMSService()