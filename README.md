# AI-Powered Invoice & Data Extraction Pipeline

A backend Python automation tool that extracts structured data from unstructured F&B supplier invoices using LLMs and stores them directly into a relational database.

## Problem & Solution
- **Problem:** Hospitality and F&B businesses receive unformatted supplier bills, requiring tedious manual data entry.
- **Solution:** This pipeline ingests messy invoice text, uses OpenAI LLM structured outputs with Pydantic validation to extract line items and totals, and commits records into an SQLite database (`invoices.db`).

## Tech Stack
- Python 3.x
- OpenAI API & Pydantic
- SQLite
