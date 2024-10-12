import csv
import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor,as_completed
import time

# for extracting all the case laws as well as legislative laws.

def extract_text_from_akoma_ntoso(url):
    """Extracts text from the 'akoma-ntoso' div in the webpage at the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the div with class 'akoma-ntoso' and extract the text
        akoma_ntoso_div = soup.find('div', class_='akoma-ntoso')
        if akoma_ntoso_div:
            return akoma_ntoso_div.get_text(separator='\n')
        else:
            print(f"No 'akoma-ntoso' div found in {url}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_section_text_to_file(text, section_number):
    """Saves the extracted text to a file named section_<section_number>.txt in the 'acts' folder."""
    folder_name = 'acts'
    os.makedirs(folder_name, exist_ok=True)  # Create the folder if it doesn't exist

    file_name = os.path.join(folder_name, f'section_{section_number}.txt')
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(text)  # Write all text at once
    print(f"Section {section_number} saved to {file_name}")

def process_csv_and_extract_sections(csv_file_path, max_workers,delay):
    """Reads the CSV file, extracts URLs and section titles, and fetches the content concurrently."""
    urls = []
    sections = []

    # Read the CSV file and store URLs and sections in lists
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urls.append(row['url'])  # Adjust based on your CSV header
            sections.append(row['title'])  # Adjust based on your CSV header
    start_time =time.time()
    # Use ThreadPoolExecutor to fetch content concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(extract_text_from_akoma_ntoso, url): section for url, section in zip(urls, sections)}

        for future in as_completed(futures):
            section = futures[future]
            try:
                extracted_text = future.result()
                if extracted_text:
                    save_section_text_to_file(extracted_text, section)
                else:
                    print(f"Failed to extract section: {section}")
            except Exception as e:
                print(f"Error processing section {section}: {e}")
            
            # Introduce a delay between requests
            time.sleep(delay)
    

    elapsed_time = time.time() - start_time
    processed_count = len(sections)
    estimated_total_time = (elapsed_time / processed_count) * len(urls)
    remaining_time = estimated_total_time - elapsed_time

    print(f"Elapsed Time: {elapsed_time:.2f} seconds")
    print(f"Estimated Remaining Time: {remaining_time:.2f} seconds")

# Example usage
csv_file = 'indian_laws_and_acts_v2.csv'  # Path to your CSV file
process_csv_and_extract_sections(csv_file, max_workers=5,delay=2)  # Adjust max_workers as needed
