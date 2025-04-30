import time
import re
import unicodedata
from dataclasses import dataclass
from fake_useragent import UserAgent
from slugify import slugify
from requests_html import HTML
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options



def get_user_agent():
    return UserAgent().random


def slugify(value: str) -> str:
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def extract_price_from_string(value: str, regex=r"[\$]{1}[\d,]+\.?\d{0,2}"):
    x = re.findall(regex, value)
    return x[0] if x else None


def contains_url(text):
    url_patterns = [r"http[s]?://", r"www\.", r"\.com", r"\.net", r"\.org"]
    return any(re.search(pattern, text) for pattern in url_patterns)


def extract_reviews(review_blocks):
    all_reviews = []
    for el in review_blocks:
        span = el.find('span', first=True)
        if span:
            review_text = span.text.strip()
            if not contains_url(review_text):
                all_reviews.append(review_text)
    return all_reviews


def clean_price(val):
    if not val:
        return None
    try:
        return float(val.replace("$", "").replace(",", "").strip())
    except ValueError:
        return None


@dataclass
class Scraper:
    url: str = None
    asin: str = None
    endless_scroll: bool = False
    endless_scroll_time: int = 5
    driver = None
    html_obj = None

    def __post_init__(self):
        if not self.url and self.asin:
            self.url = f"https://www.amazon.com/dp/{self.asin}"
        if not self.url:
            raise ValueError("Provide either a valid URL or ASIN.")

    def get_driver(self):
        if self.driver is None:
            options = uc.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument(f"user-agent={get_user_agent()}")
            self.driver = uc.Chrome(options=options)
        return self.driver

    def perform_endless_scroll(self, driver):
        if not self.endless_scroll:
            return
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.endless_scroll_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_html_obj(self):
        if self.html_obj is None:
            html_str = self.get()
            self.html_obj = HTML(html=html_str)
        return self.html_obj

    def get(self):
        driver = self.get_driver()
        driver.get(self.url)
        time.sleep(5)  # Allow time for CAPTCHA to potentially show up

        if "captcha" in driver.current_url.lower():
            print("⚠️ CAPTCHA detected! Consider using a proxy or rotating IPs.")
            driver.quit()
            raise Exception("CAPTCHA encountered.")

        if self.endless_scroll:
            self.perform_endless_scroll(driver)
        else:
            time.sleep(3)
        return driver.page_source

    def extract_element_text(self, css_selector):
        html = self.get_html_obj()
        el = html.find(css_selector, first=True)
        return el.text.strip() if el else ""

    def extract_tables(self):
        html = self.get_html_obj()
        return html.find("table")

    def extract_table_dataset(self, tables) -> dict:
        dataset = {}
        for table in tables:
            for tbody in table.element.getchildren():
                for tr in tbody.getchildren():
                    row = [col.text_content().strip() for col in tr.getchildren() if col.text_content().strip()]
                    if len(row) != 2:
                        continue
                    key, value = row
                    print(key, value)
                    key = slugify(key).replace("-", "_")
                    if key in dataset:
                        continue
                    if "$" in value:
                        dataset[key] = extract_price_from_string(value)
                        dataset[f"{key}_raw"] = value
                    else:
                        dataset[key] = value
        return dataset

    def scrape(self):
        html = self.get_html_obj()

        title = self.extract_element_text("#productTitle")
        price = (
            self.extract_element_text("#priceblock_ourprice") or
            self.extract_element_text("#priceblock_dealprice")
        )
        price_str = clean_price(price)

        # Extract image URL
        img_wrapper = html.find("#imgTagWrapperId img", first=True)
        image_url = img_wrapper.attrs.get("src") if img_wrapper else None

        # Extract rating and total reviews
        rating = None
        total_reviews = None
        customer_reviews = html.find("#acrCustomerReviewText", first=True)
        if customer_reviews:
            review_text = customer_reviews.text.strip()
            match = re.search(r'([\d,]+)', review_text)
            if match:
                total_reviews = int(match.group(1).replace(',', ''))

        rating_element = html.find("i.a-icon-star span.a-icon-alt", first=True)
        if rating_element:
            rating = rating_element.text.strip()

        # Extract reviews
        review_blocks = html.find('[data-hook="review-collapsed"]')
        reviews = extract_reviews(review_blocks)

        tables = self.extract_tables()
        specs = self.extract_table_dataset(tables)
        price = specs.get("price_raw")
        price_str = clean_price(price)
        total = specs.get("total_raw")
        total_str = clean_price(total)
        return {
            "title": title,
            "price": price_str,
            "total": total_str,
            "image_url": image_url,
            "rating": rating,
            "total_reviews": total_reviews,
            "reviews": reviews,
            # **specs
        }



# import time
# import re
# from dataclasses import dataclass
# import undetected_chromedriver as uc
# from requests_html import HTML
# from slugify import slugify
# from fake_useragent import UserAgent

# def get_user_agent():
#     """Return a random User-Agent string."""
#     return UserAgent().random

# def extract_price_from_string(value: str, regex=r"[\$]{1}[\d,]+\.?\d{0,2}"):
#     """Extract price from a string using regex."""
#     x = re.findall(regex, value)
#     return x[0] if x else None

# def contains_url(text):
#     """Check if a string contains a URL."""
#     url_patterns = [r"http[s]?://", r"www\.", r"\.com", r"\.net", r"\.org"]
#     return any(re.search(pattern, text) for pattern in url_patterns)

# def extract_reviews(review_blocks):
#     """Extract reviews from review blocks."""
#     all_reviews = []
#     for el in review_blocks:
#         span = el.find('span', first=True)
#         if span:
#             review_text = span.text.strip()
#             if not contains_url(review_text):
#                 all_reviews.append(review_text)
#     return all_reviews

# @dataclass
# class Scraper:
#     url: str = None
#     asin: str = None
#     endless_scroll: bool = False
#     endless_scroll_time: int = 5
#     driver = None
#     html_obj = None

#     def __post_init__(self):
#         # If ASIN is provided, construct the URL
#         if not self.url and self.asin:
#             self.url = f"https://www.amazon.com/dp/{self.asin}"
#         if not self.url:
#             raise ValueError("Provide either a valid URL or ASIN.")
        
#         # Make sure the URL is valid
#         if not self.url.startswith('http'):
#             raise ValueError(f"Invalid URL: {self.url}")

#     def get_driver(self):
#         if self.driver is None:
#             options = uc.ChromeOptions()
#             options.add_argument("--headless")
#             options.add_argument("--no-sandbox")
#             options.add_argument("--disable-blink-features=AutomationControlled")
#             options.add_argument(f"user-agent={get_user_agent()}")
#             self.driver = uc.Chrome(options=options)
#         return self.driver

#     def perform_endless_scroll(self, driver):
#         if not self.endless_scroll:
#             return
#         last_height = driver.execute_script("return document.body.scrollHeight")
#         while True:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(self.endless_scroll_time)
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height

#     def get_html_obj(self):
#         if self.html_obj is None:
#             html_str = self.get()
#             self.html_obj = HTML(html=html_str)
#         return self.html_obj

#     def get(self):
#         driver = self.get_driver()
#         driver.get(self.url)
#         time.sleep(5)  # Allow time for CAPTCHA to potentially show up

#         if "captcha" in driver.current_url.lower():
#             print("⚠️ CAPTCHA detected! Consider using a proxy or rotating IPs.")
#             driver.quit()
#             raise Exception("CAPTCHA encountered.")

#         if self.endless_scroll:
#             self.perform_endless_scroll(driver)
#         else:
#             time.sleep(3)
#         return driver.page_source

#     def extract_element_text(self, css_selector):
#         html = self.get_html_obj()
#         el = html.find(css_selector, first=True)
#         return el.text.strip() if el else ""

#     def extract_tables(self):
#         html = self.get_html_obj()
#         return html.find("table")

#     def extract_table_dataset(self, tables) -> dict:
#         dataset = {}
#         for table in tables:
#             for tbody in table.element.getchildren():
#                 for tr in tbody.getchildren():
#                     row = [col.text_content().strip() for col in tr.getchildren() if col.text_content().strip()]
#                     if len(row) != 2:
#                         continue
#                     key, value = row
#                     print(key, value)
#                     key = slugify(key).replace("-", "_")
#                     if key in dataset:
#                         continue
#                     if "$" in value:
#                         dataset[key] = extract_price_from_string(value)
#                         dataset[f"{key}_raw"] = value
#                     else:
#                         dataset[key] = value
#         return dataset

#     def scrape(self):
#         html = self.get_html_obj()

#         title = self.extract_element_text("#productTitle")
#         price = (
#             self.extract_element_text("#priceblock_ourprice") or
#             self.extract_element_text("#priceblock_dealprice")
#         )

#         # Extract image URL
#         img_wrapper = html.find("#imgTagWrapperId img", first=True)
#         image_url = img_wrapper.attrs.get("src") if img_wrapper else None

#         # Extract rating and total reviews
#         rating = None
#         total_reviews = None
#         customer_reviews = html.find("#acrCustomerReviewText", first=True)
#         if customer_reviews:
#             review_text = customer_reviews.text.strip()
#             match = re.search(r'([\d,]+)', review_text)
#             if match:
#                 total_reviews = int(match.group(1).replace(',', ''))

#         rating_element = html.find("i.a-icon-star span.a-icon-alt", first=True)
#         if rating_element:
#             rating = rating_element.text.strip()

#         # Extract reviews
#         review_blocks = html.find('[data-hook="review-collapsed"]')
#         reviews = extract_reviews(review_blocks)

#         tables = self.extract_tables()
#         specs = self.extract_table_dataset(tables)
#         total = specs.get("total_raw")
#         # print(total_price)
#         print("Total Raw:", specs.get("total_raw"))
#         # for i, x in enumerate(dict(specs).items()):
#         #     print(i, x.get('total_raw'))
#         #     print(i, x)
#         return {
#             "title": title,
#             "price": price,
#             "total": total,
#             "image_url": image_url,
#             "rating": rating,
#             "total_reviews": total_reviews,
#             "reviews": reviews,
#             # **specs
#         }


