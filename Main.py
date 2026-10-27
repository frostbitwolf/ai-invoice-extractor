import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

# 1. .env file nunchi environment variables ni load chestundi
load_dotenv()

# 2. OpenAI client ni secure ga initialize chestundi (.env lo unna key automatically teesukuntundi)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 3. Invoice data structure ki Pydantic model (nee requirements batti fields modify చేసుకోవచ్చు)
class InvoiceData(BaseModel):
    invoice_number: str
    vendor_name: str
    total_amount: float
    due_date: str

def extract_invoice(invoice_text: str):
    try:
        # Structured Outputs kosam OpenAI chat completion call
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert invoice extraction assistant. Extract the requested fields accurately."},
                {"role": "user", "content": f"Extract details from this invoice:\n\n{invoice_text}"},
            ],
            response_format=InvoiceData,
        )
        
        # Extracted data ni return chestundi
        extracted_data = completion.choices.message.parsed
        return extracted_data

    except Exception as e:
        print(f"Error vachindi bro: {e}")
        return None

if __name__ == "__main__":
    # Test invoice text (nee daggara unna actual invoice text/path tho replace చేసుకోవచ్చు)
    sample_invoice = "Invoice #INV-2026-001 from TechCorp Solutions. Total Amount: $250.00. Due Date: 2026-11-15."
    
    print("Extracting invoice data...")
    result = extract_invoice(sample_invoice)
    print(result)
