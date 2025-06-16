from google import genai
from pydantic import BaseModel
import enum
from .settings import GOOGLE_GENERATIVE_AI_API_KEY

class Status(enum.Enum):
    CONFIRMED = 'Confirmed'
    READY_TO_DISPATCH = 'Ready to Dispatch'
    IN_TRANSIT = 'In Transit'

class Schema(BaseModel):
    order_number: str 
    order_status: Status
    is_valid: bool

client = genai.Client(api_key=GOOGLE_GENERATIVE_AI_API_KEY)

def get_order_status_from_email(messages):
    output = []
    for message in messages:
        email_subject = message.subject
        email_body = message.snippet

        prompt = f"""
        You are a highly accurate email-processing assistant. Your task is to extract order details from emails.

        - From the email content, identify the order number.
        - Determine the order status based on the context. The status must be one of the exact values: "Confirmed", "Ready to Dispatch", or "In Transit".
        - If you cannot confidently identify both an order number and a valid status, you must set `is_valid` to false.

        Example of your task:

        Email Subject: Update on Order 7842
        Email Body: Hello team, your order 7842 has just been shipped and is on its way.

        Your analysis for the above email should result in:
        {{
        "order_number": "7842",
        "order_status": "In Transit",
        "is_valid": true
        }}

        Now, analyze the following email and provide the structured data.

        Email Subject: {email_subject}
        Email Body: {email_body}
        """

        # Step 5: Call Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Schema,
            }
        )
        print(response.text)
        my_order = response.parsed
        print(my_order.order_number, type(my_order))
        parsed = {"order_number": my_order.order_number, "order_status": my_order.order_status, "is_valid":my_order.is_valid}
        output.append(parsed)
    return output