import requests
from bs4 import BeautifulSoup
import json
import csv
import time

BASE_URL = "https://www.megekko.nl"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}



def scrape_megekko(url):
    """
    Scrapes all product details from a given subcategory URL.
    """
    products = []
    page = 1

    paginated_url = f"{url}?f=f_vrrd-3_s-populair_pp-250_p-1_d-list_cf-"
    response = requests.get(paginated_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch page {page} of {url}, status code: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all products using the schema.org Product markup
    subcategory_div = soup.find("div", class_="blocks_grid")
    subcateogries = subcategory_div.find_all('div')
    if not subcateogries:
        print("No subcategories found, stopping scraping")

    for subcategory in subcateogries:
        product_data = {}

        link = subcategory.find("a")

        url = BASE_URL + link["href"] if link and link.has_attr("href") else None

        subcateogry_products = requests.get(url, headers=HEADERS)
        subcategory_soup = BeautifulSoup(subcateogry_products.text, "html.parser")

        product_elements = subcategory_soup.find_all(attrs={"itemtype": "http://schema.org/Product"})
        if not product_elements:
            print("No products found, stopping scraping")


        for prod in product_elements:

            # Extract metadata
            meta_tags = ["sku", "image", "name"]
            for tag in meta_tags:
                meta = prod.find("meta", {"itemprop": tag})
                product_data[tag] = meta["content"] if meta and meta.has_attr("content") else None

            # Extract brand
            ''' brand_container = prod.find(attrs={"itemprop": "brand"})
            if brand_container:
                brand_meta = brand_container.find("meta", {"itemprop": "name"})
                product_data["brand"] = brand_meta["content"] if brand_meta and brand_meta.has_attr("content") else None
            else:
                product_data["brand"] = None'''

            # Extract offer details
            offer = prod.find(attrs={"itemprop": "offers"})
            offer_data = {}
            if offer:
                offer_meta_tags = ["url", "priceCurrency", "itemCondition", "price", "priceValidUntil", "availability"]
                for tag in offer_meta_tags:
                    meta = offer.find("meta", {"itemprop": tag})
                    offer_data[tag] = meta["content"] if meta and meta.has_attr("content") else None
            product_data["offer"] = offer_data

            final_url = requests.get(offer_data["url"], headers=HEADERS)
            product_soup = BeautifulSoup(final_url.text, "html.parser")

            specs = {}
            specs_container = product_soup.find(id="prd_rawspecs")

            if specs_container:
                for grid in specs_container.find_all(class_="prd_specsgrid"):
                    spec_divs = grid.find_all("div")
                    for i in range(0, len(spec_divs)-1, 2):
                        key = spec_divs[i].get_text(strip=True)
                        value = spec_divs[i+1].get_text(strip=True)
                        specs[key] = value
            product_data["specs"] = specs

            '''# Extract specifications
            specs = {}
            specs_container = prod.find(class_="prdSpecs")
            if specs_container:
                for spec in specs_container.find_all(class_="prdSpec"):
                    spec_divs = spec.find_all("div")
                    if len(spec_divs) >= 2:
                        key = spec_divs[0].get_text(strip=True)
                        value = spec_divs[1].get_text(strip=True)
                        specs[key] = value
            product_data["specs"] = specs
            '''
            # Extract subheader
            subheader = prod.find(class_="prdSubheader")
            product_data["subheader"] = subheader.get_text(strip=True) if subheader else None

            products.append(product_data)
    return products


def get_subcategories(category_url):
    """
    Extracts subcategory links from a given category URL.
    """
    response = requests.get(category_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch category page: {category_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    subcategories = []

    subcategory_blocks = soup.find_all('div', class_='navblock_v5')

    for block in subcategory_blocks:
        try:
            subcategory_title = block.find('h2', class_='block_title').get_text(strip=True)
            subcategory_link = BASE_URL + block.find('a')['href']
            subcategories.append({"title": subcategory_title, "url": subcategory_link})
        except AttributeError:
            continue

    return subcategories



'''def save_to_csv(products, filename="scraped_data.csv"):
    """
    Saves scraped product data to a CSV file.
    """
    if not products:
        print("No products to save.")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products) '''

    #print(f"Data saved to {filename}")

def scrape_all_products(category_url):
    """
    Scrapes products from all subcategories under a given category.
    """
    subcategories = []
    for subcategory in get_subcategories(category_url):
        if subcategory['title'] in ["Processoren", "Moederborden", "Geheugen", "Videokaarten", "Behuizingen en meer", "Voedingen", "Opslag", "Koeling", "SSD (Solid state drive)", "Hard disks"]:
            subcategories.append(subcategory)
    all_products = {}

    for subcategory in subcategories:
        #print(f"Scraping subcategory: {subcategory['title']} ({subcategory['url']})")
        products = scrape_megekko(subcategory['url'])
        all_products[subcategory['title']] = products

    # Save to JSON
    with open("megekko_products-test.json", "w", encoding="utf-8") as json_file:
        json.dump(all_products, json_file, ensure_ascii=False, indent=2)

    print("✅ Scraping completed! Data saved to JSON and CSV.")

# Run the scraper

def main():
    category_url = "https://www.megekko.nl/Computer/Componenten/"
    scrape_all_products(category_url)


if __name__ == "__main__":
    main()
