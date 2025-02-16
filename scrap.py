import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Load the JSON file
with open("data_kelas.json", "r", encoding="utf-8") as file:
    kelas_data = json.load(file)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open the browser
driver.get("https://akademik.its.ac.id/")

while True:
    # print(driver.current_url)
    if "https://akademik.its.ac.id/home.php" in driver.current_url:
        print('Authenticated')
        break
    time.sleep(1)

# Create an output directory if not exists
output_dir = "scraped_results"
os.makedirs(output_dir, exist_ok=True)

# Iterate over each course and its classes
for course in kelas_data:
    scrap = course["scrap"]
    if not scrap:
        print(f"⚠ Scraping is disabled for {course['mkID']}")
        continue
    mkJur = course["mkJur"]
    mkSem = course["mkSem"]
    mkID = course["mkID"]
    mkThn = course["mkThn"]

    for kelas in course["kelas"]:
        # Construct the URL dynamically
        url = f"https://akademik.its.ac.id/lv_peserta.php?mkJur={mkJur}&mkID={mkID}&mkSem={mkSem}&mkThn={mkThn}&mkKelas={kelas}&mkThnKurikulum=2023"
        print(f"Scraping: {url}")

        # Go to the page
        driver.get(url)
        # time.sleep(5)  # Let the page load

        # Extract page content
        html = driver.page_source

        # Parse HTML
        soup = BeautifulSoup(html, "html.parser")

        # Find all tables and select the second one
        tables = soup.find_all("table")
        if len(tables) < 2:
            print(f"⚠ No data found for {mkID} {kelas}")
            continue  # Skip to the next class

        title = tables[0].find_all("tr")[1].find("td").text.strip()

        second_table = tables[1]

        # Extract rows (skip the header)
        rows = second_table.find_all("tr")[1:]
        data = []

        # Extract data from rows
        for row in rows:
            cols = [col.text.strip() for col in row.find_all("td")]
            if cols:
                data.append({
                    "NO": int(cols[0]),
                    "NRP": cols[1],
                    "Nama": cols[2]
                })

        # Convert data to JSON
        json_output = json.dumps(data, indent=2, ensure_ascii=False)

        # Generate output filename
        filename = f"{title}.json"
        filepath = os.path.join(output_dir, filename)

        # Save JSON to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_output)

        print(f"✅ Data saved to {filepath}")

print("🎉 Scraping completed!")

# Close the browser
driver.quit()
