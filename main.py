import os
import sqlite3
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI()

class LineItem(BaseModel):
    item_name: str = Field(description="Name of the product or service")
    quantity: int = Field(description="Quantity purchased")
    unit_price: float = Field(description="Price per single unit")
    total_price: float = Field(description="Total price for this line item")

class InvoiceData(BaseModel):
    vendor_name: str = Field(description="Name of the supplier or vendor")
    invoice_date: str = Field(description="Date of the invoice YYYY-MM-DD")
    line_items: List[LineItem]
    tax_amount: float = Field(description="Total tax amount applied")
    grand_total: float = Field(description="Final total including tax")

def init_db():
    conn = sqlite3.connect("invoices.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extracted_invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_name TEXT,
            invoice_date TEXT,
            grand_total REAL
        )
    ''')
    conn.commit()
    conn.close()

def extract_invoice_data(raw_text: str) -> InvoiceData:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert data extraction agent. Extract structured data from the given unstructured invoice text."},
            {"role": "user", "content": raw_text}
        ],
        response_format=InvoiceData,
    )
    return completion.choices.message.parsed

def save_to_db(data: InvoiceData):
    conn = sqlite3.connect("invoices.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO extracted_invoices (vendor_name, invoice_date, grand_total)
        VALUES (?, ?, ?)
    ''', (data.vendor_name, data.invoice_date, data.grand_total))
    conn.commit()
    conn.close()
    print("Successfully saved invoice data to SQLite database!")

if __name__ == "__main__":
    init_db()
    sample_invoice = """
    Hey there, here is the bill from Gourmet Foods Supplier LLC for order on 2026-10-24.
    Items supplied:
    - 10x Organic Olive Oil bottles @ $15.00 each = $150.00
    - 5x Artisan Truffle Cheese blocks @ $20.00 each = $100.00
    Subtotal before tax. Tax applied was 12.50. 
    Final Total to pay: $262.50. Thanks!
    """
    print("Processing messy invoice text...")
    extracted_result = extract_invoice_data(sample_invoice)
    print("\n--- Extracted Structured JSON ---")
    print(extracted_result.model_dump_json(indent=2))
    save_to_db(extracted_result)

