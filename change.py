import requests
from bs4 import BeautifulSoup
import hashlib
import os

# Define the URL of the web page you want to monitor
url = "https://www.gov.hk/en/nonresidents/visarequire/visasentrypermits/applyvisit_transit.htm"

# Define the file path to store the page content
data_folder = "web_page_data"
os.makedirs(data_folder, exist_ok=True)
page_file = os.path.join(data_folder, "page_content.html")

# Function to fetch and save the web page content
def fetch_and_save_page(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)

# Function to calculate the MD5 hash of a file
def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to compare the current and previous page content
def compare_pages(current_file, previous_file):
    current_md5 = calculate_md5(current_file)
    previous_md5 = calculate_md5(previous_file)
    return current_md5 != previous_md5

# Function to get the list of added and removed lines
def get_line_changes(string1, string2):
    from difflib import Differ
    d = Differ()
    diff = list(d.compare(string1.splitlines(), string2.splitlines()))
    added_lines = [line[2:] for line in diff if line.startswith('+ ')]
    removed_lines = [line[2:] for line in diff if line.startswith('- ')]
    return added_lines, removed_lines

# Check if today's page content is different from yesterday's
fetch_and_save_page(url, page_file)

previous_page_file = os.path.join(data_folder, "previous_page_content.html")
if os.path.exists(previous_page_file):
    with open(page_file, "r", encoding="utf-8") as current_file:
        current_content = current_file.read()

    with open(previous_page_file, "r", encoding="utf-8") as previous_file:
        previous_content = previous_file.read()

    added_lines, removed_lines = get_line_changes(previous_content, current_content)
    
    if compare_pages(page_file, previous_page_file):
        print("Trang web đã thay đổi so với ngày hôm trước!")
        print("Các dòng thêm:")
        print("\n".join(added_lines))
        print("\nCác dòng bị xóa:")
        print("\n".join(removed_lines))
    else:
        print("Trang web vẫn giống như ngày hôm trước.")
else:
    print("Không tìm thấy dữ liệu trước đó. Lưu trữ dữ liệu hôm nay như là tham chiếu ban đầu.")

    # Save today's data as the initial reference
    os.rename(page_file, previous_page_file)
