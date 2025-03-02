# -*- coding: utf-8 -*-
"""RFP_LLM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WGZNbpzzbZ2vBPgF_JjEctNA5TggsAvJ
"""

!pip install pdfplumber

pip install groq

import pdfplumber
from bs4 import BeautifulSoup
import pandas as pd

def process_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        print("PDF Text Extracted Successfully.")
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def process_html(file_path):
    """
    Extract text from an HTML file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator="\n")
        title = soup.find('title').text if soup.find('title') else "No Title Found"
        print(f"HTML Title Extracted: {title}")
        return text
    except Exception as e:
        print(f"Error processing HTML: {e}")
        return None

def extract_info_with_groq(document_text, model="llama-3.3-70b-versatile"):
    """
    Send document text to Groq API and extract structured information.
    """
    prompt = f"""
    Extract the following information from this document:
    - Bid Number
    - Title
    - Due Date
    - Bid Submission Type
    - Term of Bid
    - Pre-Bid Meeting
    - Installation
    - Bid Bond Requirement
    - Delivery Date
    - Payment Terms
    - Any Additional Documentation Required
    - MFG for Registration
    - Contract or Cooperative to use
    - Model_no
    - Part_no
    - Product
    - contact_info
    - company_name
    - Bid Summary
    - Product Specification

    Document:
    {document_text}
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in extracting structured data."},
                {"role": "user", "content": prompt},
            ],
            model=model,
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error querying Groq API: {e}")
        return None

def save_to_table(extracted_info, output_file):
    """
    Save extracted information into a CSV or table format.
    """
    try:
        data = {"Field": [], "Value": []}
        for line in extracted_info.split("\n"):
            if ":" in line:
                field, value = line.split(":", 1)
                data["Field"].append(field.strip())
                data["Value"].append(value.strip())
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving data to table: {e}")

def process_document(file_path, file_type, output_file):
    """
    Process a single document and save the extracted information to a table.
    """
    if file_type == "pdf":
        document_text = process_pdf(file_path)
    elif file_type == "html":
        document_text = process_html(file_path)
    else:
        print("Unsupported file type.")
        return

    if document_text:
        extracted_info = extract_info_with_groq(document_text)
        if extracted_info:
            save_to_table(extracted_info, output_file)
        else:
            print("No information extracted.")
    else:
        print("No text extracted from document.")

# Example usage:
# For a PDF file
process_document("/content/Addendum 1 RFP JA-207652 Student and Staff Computing Devices.pdf", "pdf", "output_pdf.csv")

# For an HTML file
process_document("//content/Student and Staff Computing Devices __SOURCING #168884__ - Bid Information - {3} _ BidNet Direct.html", "html", "output_html.csv")

pip install python-dotenv

import os
from groq import Groq
import pdfplumber
from bs4 import BeautifulSoup

# Set up Groq API client
api_key = "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"  # Replace with your actual API key
client = Groq(api_key=api_key)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

# Function to parse HTML and extract information
def extract_info_from_html(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('title').text if soup.find('title') else "No title found"
        return {"title": title, "html_content": html_content}
    except Exception as e:
        print(f"Error extracting information from HTML: {e}")
        return None

# Function to query Groq API
def extract_info_with_groq(text):
    prompt = f"""
    Extract the following information from this document:
    - Bid Number
    - Title
    - Due Date
    - Bid Submission Type
    - Term of Bid
    - Pre-Bid Meeting
    - Installation
    - Bid Bond Requirement
    - Delivery Date
    - Payment Terms
    - Any Additional Documentation Required
    - MFG for Registration
    - Contract or Cooperative to use
    - Model_no
    - Part_no
    - Product
    - contact_info
    - company_name
    - Bid Summary
    - Product Specification

    Document:
    {text}
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in extracting structured data."},
                {"role": "user", "content": prompt},
            ],
            model="llama-3.3-70b-versatile",  # Replace with the desired model
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error querying Groq API: {e}")
        return None

# Paths to input files
pdf_path = "/content/Addendum 1 RFP JA-207652 Student and Staff Computing Devices.pdf"
html_path = "/content/Student and Staff Computing Devices __SOURCING #168884__ - Bid Information - {3} _ BidNet Direct.html"

# Extract text from PDF
pdf_text = extract_text_from_pdf(pdf_path)
if pdf_text:
    print("PDF Text Extracted Successfully.")

# Extract information from HTML
html_info = extract_info_from_html(html_path)
if html_info:
    print(f"HTML Title Extracted: {html_info['title']}")

# Combine PDF and HTML content for Groq
combined_text = pdf_text + "\n\n" + html_info["html_content"] if pdf_text and html_info else pdf_text or html_info

# Query Groq API for structured data
if combined_text:
    extracted_info = extract_info_with_groq(combined_text)
    print("Extracted Information:")
    print(extracted_info)
else:
    print("No content to process with Groq.")

import pdfplumber
from bs4 import BeautifulSoup
import pandas as pd

def process_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        print("PDF Text Extracted Successfully.")
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def process_html(file_path):
    """
    Extract text from an HTML file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator="\n")
        title = soup.find('title').text if soup.find('title') else "No Title Found"
        print(f"HTML Title Extracted: {title}")
        return text
    except Exception as e:
        print(f"Error processing HTML: {e}")
        return None

def extract_info_with_groq(document_text, model="llama-3.3-70b-versatile"):
    """
    Send document text to Groq API and extract structured information.
    """
    prompt = f"""
    Extract the following information from this document:
    - Bid Number
    - Title
    - Due Date
    - Bid Submission Type
    - Term of Bid
    - Pre-Bid Meeting
    - Installation
    - Bid Bond Requirement
    - Delivery Date
    - Payment Terms
    - Any Additional Documentation Required
    - MFG for Registration
    - Contract or Cooperative to use
    - Model_no
    - Part_no
    - Product
    - contact_info
    - company_name
    - Bid Summary
    - Product Specification

    Document:
    {document_text}
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in extracting structured data."},
                {"role": "user", "content": prompt},
            ],
            model=model,
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error querying Groq API: {e}")
        return None

def save_to_table(extracted_info, output_file):
    """
    Save extracted information into a CSV or table format.
    """
    try:
        data = {"Field": [], "Value": []}
        for line in extracted_info.split("\n"):
            if ":" in line:
                field, value = line.split(":", 1)
                data["Field"].append(field.strip())
                data["Value"].append(value.strip())
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving data to table: {e}")

def process_document(file_path, file_type, output_file):
    """
    Process a single document and save the extracted information to a table.
    """
    if file_type == "pdf":
        document_text = process_pdf(file_path)
    elif file_type == "html":
        document_text = process_html(file_path)
    else:
        print("Unsupported file type.")
        return

    if document_text:
        extracted_info = extract_info_with_groq(document_text)
        if extracted_info:
            save_to_table(extracted_info, output_file)
        else:
            print("No information extracted.")
    else:
        print("No text extracted from document.")

# Example usage:
# For a PDF file
process_document("/content/Addendum 1 RFP JA-207652 Student and Staff Computing Devices.pdf", "pdf", "output_pdf.csv")

# For an HTML file
process_document("//content/Student and Staff Computing Devices __SOURCING #168884__ - Bid Information - {3} _ BidNet Direct.html", "html", "output_html.csv")

import pdfplumber
from bs4 import BeautifulSoup
import pandas as pd
import json
import requests  # Assuming you are using HTTP requests for the Groq API

# Replace with your Groq API endpoint and key
GROQ_API_URL = "https://api.groq.com/v1/extract"
API_KEY = "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"

def process_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        print("PDF Text Extracted Successfully.")
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def process_html(file_path):
    """
    Extract text from an HTML file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator="\n")
        title = soup.find('title').text if soup.find('title') else "No Title Found"
        print(f"HTML Title Extracted: {title}")
        return text
    except Exception as e:
        print(f"Error processing HTML: {e}")
        return None

def extract_info_with_groq(document_text):
    """
    Send document text to Groq API and extract structured information.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "document_text": document_text
    }

    try:
        response = requests.post(GROQ_API_URL, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()  # Assuming the API returns structured JSON data
        else:
            print(f"Error querying Groq API: {response.text}")
            return None
    except Exception as e:
        print(f"Error querying Groq API: {e}")
        return None

def save_to_json(extracted_info, output_file):
    """
    Save extracted information into a JSON format.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(extracted_info, json_file, ensure_ascii=False, indent=4)
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

def process_document(file_path, file_type, output_file):
    """
    Process a single document and save the extracted information to a JSON file.
    """
    if file_type == "pdf":
        document_text = process_pdf(file_path)
    elif file_type == "html":
        document_text = process_html(file_path)
    else:
        print("Unsupported file type.")
        return

    if document_text:
        extracted_info = extract_info_with_groq(document_text)
        if extracted_info:
            save_to_json(extracted_info, output_file)
        else:
            print("No information extracted.")
    else:
        print("No text extracted from document.")

# Example usage:
# For a PDF file
process_document("/content/Addendum 1 RFP JA-207652 Student and Staff Computing Devices.pdf", "pdf", "output_pdf.json")

# For an HTML file
process_document("//content/Student and Staff Computing Devices __SOURCING #168884__ - Bid Information - {3} _ BidNet Direct.html", "html", "output_html.json")