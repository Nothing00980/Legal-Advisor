import os
import re
import pdfplumber

# for extracting all ipc sections.
# Step 1: Define paths and parameters
pdf_path = 'Indian Penal Code Book.pdf'  # Path to your PDF
output_folder = 'ipc_sections'  # Folder to save sections
chunk_size = 100  # Number of pages per chunk
section_counter = 1  # To keep track of section number

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define the start and end delimiters for sections
start_delimiter = r'\[s\s\d+\]'  # Regex to match "[s <number>]"
end_delimiter = r'THE INDIAN PENAL CODE'  # End phrase

# Step 2: Extract and save sections in chunks
with pdfplumber.open(pdf_path) as pdf:
    total_pages = len(pdf.pages)
    
    for start in range(0, total_pages, chunk_size):
        end = min(start + chunk_size, total_pages)  # Ensure end doesn't exceed total pages
        
        # Extract text for the current chunk
        chunk_text = ''
        for page in pdf.pages[start:end]:
            chunk_text += page.extract_text() + '\n'
        
        # Step 3: Search for sections using regex
        sections = re.split(start_delimiter, chunk_text)  # Split by "[s <number>]"
        
        # Skip the first entry if it is empty (text before the first "[s %d]")
        for section in sections[1:]:
            # Extract content until the end delimiter
            content = re.split(end_delimiter, section)[0].strip()
            
            # Save each section as a separate file
            if content:
                file_name = f'section_{section_counter}.txt'
                file_path = os.path.join(output_folder, file_name)
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                section_counter += 1  # Increment section counter

print(f"Sections saved in folder: {output_folder}")
