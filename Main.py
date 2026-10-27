import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class InvoiceData(BaseModel):
    invoice_number: str
    vendor_name: str
    total_amount: float
    due_date: str

def extract_invoice(invoice_text: str):
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert invoice extraction assistant. Extract the requested fields accurately."
                },
                {
                    "role": "user",
                    "content": f"Extract details from this invoice:\n\n{invoice_text}"
                },
            ],
            response_format=InvoiceData,
        )
        
        extracted_data = completion.choices[0].message.parsed
        return extracted_data

    except Exception as e:
        print(f"Error vachindi bro: {e}")
        return None

if __name__ == "__main__":
    sample_invoice = "Invoice #INV-2026-001 from TechCorp Solutions. Total Amount: $250.00. Due Date: 2026-11-15."
    
    print("Extracting invoice data...")
    result = extract_invoice(sample_invoice)
    print(result)
