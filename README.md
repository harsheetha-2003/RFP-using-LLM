# RFP-using-LLM
The goal is to extract structured information similar to the a required structure:
Document Text Extraction and Information Extraction using Groq API
This Python script is designed to extract text from PDF and HTML documents and use the Groq API to extract structured information from them. It then saves the extracted data into a CSV file for further analysis.

Required Libraries:
To run the script, you'll need to install the following Python libraries:

pdfplumber - Used for extracting text from PDF files.
BeautifulSoup - Part of the bs4 package, used for parsing and extracting text from HTML files.
pandas - Used for organizing extracted data into tabular format and saving it as a CSV file.
Install the required libraries using pip:

bash
Copy
Edit
pip install pdfplumber beautifulsoup4 pandas
Functions:
1. process_pdf(file_path)
Purpose: Extracts text from a PDF file.
Input: File path of the PDF file.
Output: Extracted text from the PDF document.
Error Handling: If an error occurs during extraction, an error message will be printed.
2. process_html(file_path)
Purpose: Extracts text and title from an HTML file.
Input: File path of the HTML file.
Output: Extracted text and HTML title (if available).
Error Handling: If an error occurs during extraction, an error message will be printed.
3. extract_info_with_groq(document_text, model="llama-3.3-70b-versatile")
Purpose: Sends the extracted document text to the Groq API to extract structured information.
Input: Text content of the document.
Output: Structured information based on a predefined prompt (e.g., Bid Number, Due Date, etc.).
Error Handling: If there is an issue with the API call, an error message will be printed.
4. save_to_table(extracted_info, output_file)
Purpose: Saves the extracted structured information into a CSV file.
Input: Extracted information (text), output file name.
Output: Saves the information in a CSV file with two columns: "Field" and "Value".
5. process_document(file_path, file_type, output_file)
Purpose: A wrapper function that processes a single document (either PDF or HTML), extracts text, sends it to Groq API, and saves the extracted information into a CSV file.
Input: File path of the document, document type ("pdf" or "html"), output CSV file name.
Output: A CSV file containing the extracted information.
Example Usage:
For a PDF File:
python
Copy
Edit
process_document("/content/Addendum 1 RFP JA-207652 Student and Staff Computing Devices.pdf", "pdf", "output_pdf.csv")
For an HTML File:
python
Copy
Edit
process_document("/content/Student and Staff Computing Devices __SOURCING #168884__ - Bid Information - {3} _ BidNet Direct.html", "html", "output_html.csv")
This will extract the relevant details from the PDF or HTML document and save it as a CSV file.

Output:
The output will be saved in a CSV file with two columns:

Field: The extracted data field (e.g., "Bid Number", "Title", etc.)
Value: The corresponding value extracted from the document.
Example output CSV format:

csv
Copy
Edit
Field,Value
Bid Number,12345
Title,Student and Staff Computing Devices
Due Date,2025-01-30
...
Notes:
Ensure that the Groq API client is properly set up and authenticated before running the script.
The model "llama-3.3-70b-versatile" is used by default, but you can specify a different model if needed.
