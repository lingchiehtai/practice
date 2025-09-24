# 這段程式碼由 AI (Gemini) 協助生成，用於批次處理照片檔案。
#
# 主要功能：
#   - 讀取使用者提供的每日筆記檔案 (mynote.txt)。
#   - 根據照片的辨識內容和對應日期的筆記，透過 Gemini AI 產生描述性的關鍵字。
#   - 將這些關鍵字附加到檔案名稱中，使檔案更具意義和可搜尋性。
#   - 流程包含：解析筆記、找出需要重新命名的檔案，以及呼叫 AI 來生成新檔名。


import os
import re
import time
import google.generativeai as genai
from pathlib import Path

# --- Configuration ---
# 1. Set your API Key as an environment variable named GOOGLE_API_KEY
#    For example, in your terminal: export GOOGLE_API_KEY="YOUR_API_KEY"
API_KEY = os.getenv('GOOGLE_API_KEY')

# 2. Define the directory where your photos are located.
PHOTO_DIRECTORY = Path('.') 

# 3. Define the name of your notes file.
NOTES_FILE = 'mynote.txt'

# 4. Gemini model configuration
#MODEL_NAME = "gemini-2.5-pro"
MODEL_NAME = "gemini-2.5-flash"
GENERATION_CONFIG = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
# --- End of Configuration ---

def parse_notes(file_path):
    """
    尋找所有格式為 月/日 的日期，並將日期後面的文字視為當天的筆記內容。
    Parses the mynote.txt file and returns a dictionary mapping dates to notes.
    """
    notes = {}
    if not file_path.exists():
        print(f"Warning: Notes file '{file_path}' not found.")
        return notes

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find dates (e.g., 9/10, 12/31) and the text that follows
    date_pattern = re.compile(r'(\d{1,2}/\d{1,2})')
    sections = date_pattern.split(content)
    
    # The first element is the text before any date, so we skip it.
    # Then we iterate in pairs: (date, text).
    for i in range(1, len(sections), 2):
        date_key = sections[i]
        note_text = sections[i+1].strip()
        notes[date_key] = note_text
        
    return notes

def get_files_to_rename(directory):
    """
    找出尚未被重新命名的圖片檔
    Finds all image files in the directory that have not been renamed yet.
    A file is considered "not renamed" if its name is in the format YYYY-MM-DD_NUM.ext
    """
    unnamed_files = []
    # This regex matches filenames like '2025-09-10_51.jpg' but not '2025-09-10_51_keyword.jpg'
    # It ensures we don't try to rename files that already have descriptive keywords.
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}_\d{1,}\.(jpg|jpeg|png)$', re.IGNORECASE)
    
    for file_path in directory.iterdir():
        if file_path.is_file() and pattern.match(file_path.name):
            unnamed_files.append(file_path)
            
    return sorted(unnamed_files)

def generate_new_filename(model, image_path, notes_for_date):
    """
    Uses the Gemini API to generate a new filename based on the image and notes.
    Includes retry logic for API errors.
    """
    original_stem = image_path.stem
    original_suffix = image_path.suffix
    
    prompt = f"""
    You are an expert file renamer. Your task is to analyze the provided image and the context from the text notes for that day.
    Based on this analysis, generate a new, descriptive filename.

    **Instructions:**
    1.  The new filename MUST start with the exact original name: `{original_stem}`.
    2.  Append descriptive keywords based on the image content and notes. Separate keywords with underscores (`_`).
    3.  Do NOT change the original file extension (`{original_suffix}`).
    4.  If the notes do not seem to match the image, rely only on the visual content of the image for keywords.
    5.  Your response must be ONLY the new filename and nothing else.

    **Example:**
    If the original name is `2025-09-10_052` and the image shows pants hangers from Nitori, a good response would be:
    `2025-09-10_052_宜得利_褲用衣架.jpg`

    **Context from notes for this day:**
    ---
    {notes_for_date if notes_for_date else "No notes provided for this day."} 
    ---

    Now, generate the new filename for the image provided.
    """
    
    image_file = genai.upload_file(path=str(image_path))
    
    max_retries = 10
    for i in range(max_retries):
        try:
            response = model.generate_content([prompt, image_file])
            # Clean up the response to ensure it's a valid filename
            new_name = response.text.strip().replace('\n', '')
            # Basic validation
            if new_name.startswith(original_stem) and new_name.endswith(original_suffix):
                return new_name
            else:
                print(f"  - Warning: AI returned an invalid format: '{new_name}'. Skipping.")
                return None
        except Exception as e:
            print(f"  - Error calling Gemini API: {e}")
            if "503" in str(e) and i < max_retries - 1:
                wait_time = 2 ** i
                print(f"  - Received 503 error. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("  - Max retries reached or non-retryable error. Skipping file.")
                return None
    return None

def main():
    """
    Main function to orchestrate the renaming process.
    """
    if not API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set your API key and run the script again.")
        return

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        MODEL_NAME,
        safety_settings=SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG,
    )

    print("Starting photo renaming process...")
    
    notes_path = PHOTO_DIRECTORY / NOTES_FILE
    notes_by_date = parse_notes(notes_path)
    
    files_to_process = get_files_to_rename(PHOTO_DIRECTORY)
    
    if not files_to_process:
        print("No files to rename. All images seem to have descriptive names already.")
        return

    print(f"Found {len(files_to_process)} files to rename.")

    for file_path in files_to_process:
        print(f"\nProcessing '{file_path.name}'...")
        
        # Extract date from filename (e.g., '2025-09-12' -> '9/12')
        try:
            date_parts = file_path.stem.split('_')[0].split('-')
            month = int(date_parts[1])
            day = int(date_parts[2])
            notes_key = f"{month}/{day}"
        except (IndexError, ValueError):
            print(f"  - Could not parse date from filename. Skipping.")
            continue
            
        notes_for_date = notes_by_date.get(notes_key, "")
        
        new_filename = generate_new_filename(model, file_path, notes_for_date)
        
        if new_filename:
            try:
                new_path = file_path.with_name(new_filename)
                if new_path.exists():
                    print(f"  - Error: A file named '{new_filename}' already exists. Skipping.")
                    continue
                
                file_path.rename(new_path)
                print(f"  - Renamed to: '{new_filename}'")
            except OSError as e:
                print(f"  - Error renaming file: {e}")

    print("\nRenaming process complete.")

if __name__ == "__main__":
    main()
