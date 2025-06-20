import os
import re
import time
import csv
import requests
from bs4 import BeautifulSoup

# STEP 1: Load the saved Wikipedia HTML file
with open("List of basketball films - Wikipedia.html", "rb") as file:
    page = BeautifulSoup(file, "html.parser")

# STEP 2: Get footnote references (e.g. [1])
footnotes = {}
reference_list = page.select("ol.references > li[id]")
for ref in reference_list:
    footnotes[ref["id"]] = ref.get_text(" ", strip=True)

# STEP 3: Find the table with all the movies
table = page.find("table", class_="wikitable sortable")
rows = table.find_all("tr")

# STEP 4: Set up the columns we want in our final CSV
column_names = [th.get_text(strip=True) for th in rows[0].find_all("th")]
column_names += [
    "movie_link", "director", "producer", "writer", "cast",
    "production_company", "country", "budget", "running_time", "footnote_text"
]

all_data = []
base_url = "https://en.wikipedia.org"

# STEP 5: Go through each movie row
for row in rows[1:]:
    cells = row.find_all("td")
    if not cells:
        continue

    # Step 5a: Extract footnote references before decomposing
    footnote_parts = []
    for sup in row.find_all("sup"):
        a_tag = sup.find("a")
        if a_tag and "href" in a_tag.attrs:
            foot_id = a_tag["href"].replace("#", "")
            if foot_id in footnotes:
                footnote_parts.append(footnotes[foot_id])

    footnote_text = " | ".join(footnote_parts)

    # Step 5b: Remove footnote tags so they're not in the main cell text
    for sup in row.find_all("sup"):
        sup.decompose()

    # Step 5c: Now extract the clean row text
    row_info = []
    for cell in cells:
        row_info.append(cell.get_text(" ", strip=True))

    # Pad missing cells
    while len(row_info) < len(column_names) - 11:
        row_info.append("")

    # Get movie Wikipedia link
    link = ""
    link_tag = cells[0].find("a")
    if link_tag and "href" in link_tag.attrs:
        link = base_url + link_tag["href"]

    # Append all columns including placeholders for scraped values
    row_info += [link, "", "", "", "", "", "", "", "", footnote_text]
    all_data.append(row_info)

# STEP 6: Remove rows with no Wikipedia link
all_data = [row for row in all_data if row[column_names.index("movie_link")].startswith("http")]

# STEP 7: Scrape movie info
def scrape_movie_page(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        info = soup.find("table", class_="infobox")

        if not info:
            return [""] * 8

        def get_text(label):
            header = info.find("th", string=re.compile(label, re.IGNORECASE))
            if header:
                cell = header.find_next_sibling("td")
                if cell:
                    return cell.get_text(" ", strip=True)
            return ""

        def get_cast():
            header = info.find("th", string=re.compile("starring|cast", re.IGNORECASE))
            if header:
                cell = header.find_next_sibling("td")
                if cell:
                    list_items = cell.find_all("li")
                    if list_items:
                        return ", ".join([li.get_text(strip=True) for li in list_items])
                    return cell.get_text(", ", strip=True)
            return ""

        director = get_text("Directed by")
        producer = get_text("Produced by|Production")
        writer = get_text("Written by")
        cast = get_cast()
        company = get_text("Production company|Production companies|Studio")
        country = get_text("Country")
        budget = get_text("Budget")
        runtime = get_text("Running time")

        return [director, producer, writer, cast, company, country, budget, runtime]

    except Exception as e:
        print("Error scraping:", url)
        return [""] * 8

# STEP 8: Update movie rows with scraped data
for row in all_data:
    url = row[column_names.index("movie_link")]
    print("Scraping:", url)
    details = scrape_movie_page(url)
    row[-10:-2] = details  # Fill in the 8 extra fields we made
    time.sleep(1)

# STEP 9: Write to CSV
with open("basketball_films.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(column_names)
    writer.writerows(all_data)

print("Saved: basketball_films.csv")
