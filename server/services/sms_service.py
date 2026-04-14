import os 
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class SMSService:
    def __init__(self):
        self.acc_sid=os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token=os.environ.get('TWILIO_AUTH_TOKEN')
        self.from_number=os.environ.get('TWILIO_PHONE_NUMBER')
        
        if self.acc_sid and self.auth_token and self.from_number:
            self.client=Client(self.acc_sid, self.auth_token)
        else:
            print('Credentials are not correct or not set ')
        
    def send_sms(self,to_number,message_body):
        
        """Returns tru when sends sms successfully
        otherwise false
        """
        
        if not self.client:
            return False
        
        if not to_number or not message_body:
            return False
        
        #ensure number has a +
        if not to_number.startswith('+'):
            print("Number not in international format doesn't start with { + }.")
        
        try:
            message=self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=to_number
            )
            print(f'SMS sent successfully to {to_number}. SID: {message.sid}')
            return True
        
        except TwilioRestException as e:
            print(f'Twilio API error: {e}')
            return False
        
        except Exception as e:
            print(f'Unexpected error occurred while sending SMS: {e}')

sms_service=SMSService() #GLOBAL instance
            