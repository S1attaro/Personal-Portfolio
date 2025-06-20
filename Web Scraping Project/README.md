# Summary

This project teaches how to scrape and organize movie data from a Wikipedia page about basketball films. It’s designed for students who know Python basics and want hands-on experience with web scraping.

The script starts with a saved copy of the Wikipedia page and uses BeautifulSoup to extract each movie listed in the table. It pulls out core details, cleans footnote clutter, and then follows each movie's embedded Wikipedia link to gather more information like director, producer, cast, budget, and runtime.

Both local HTML parsing and live web scraping are used to build a complete dataset. The final result is saved as a CSV that’s ready for analysis or visualization. This project shows how real-world data often needs extra steps to become usable and highlights how to combine local and online sources responsibly.
