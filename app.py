import csv
import json
import requests
import time

# 9 - fiction & literature (2876)
# 4 - business & eco products (789)
# 27 - biography & memoir products (384)
# 320 - english products
# 8322 - all books
# 1815 - digital devices
# 1801 = camera
# 1846 = laptop - pc

product_page_url = "https://tiki.vn/api/v2/products?category=27&page={}&limit=300"
product_url = "https://tiki.vn/api/v2/products/{}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
product_ids_file = "./bio-memoir-english-book-id.txt"
product_raw_data_file = "./bio-memoir-english-book.txt"
product_file = "./bio-memoir-english-file.csv"


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, indent=4)
    print(text)


def crawl_product_id():
    product_ids = []
    i = 0
    page = 1
    while (True):
        print("Crawl page: ", page)
        print('URL: ', product_page_url.format(page))

        response = requests.get(product_page_url.format(page), headers=headers)

        results = response.json()

        products = results['data']

        if (len(products) == 0):
            # if(page == 2):
            print(len(products), 'data !!! End here.')
            break

        for product in products:
            product_ids.append(str(product['id']))

        print("No. IDs: ", len(product_ids))

        if (len(product_ids) > results['paging']['total']):
            # if(page == 2):
            print('No more data !!! End here.')
            break

        i += 1
        page += 1
    return product_ids, i


def save_product_id(product_ids=[]):
    file = open(product_ids_file, "w+")
    file.write('\n'.join(product_ids))
    file.close()
    print("Save file: ", product_ids_file)


def load_product_ids():
    file = open(product_ids_file, "r")
    return file.readlines()


def crawl_product(product_ids=[]):
    product_detail_list = []
    for product_id in product_ids:
        response = requests.get(
            product_url.format(product_id), headers=headers)

        if (response.status_code == 200):
            product_detail_list.append(response.text)
            print("Crawl product: ", product_id,
                  ": ", response.status_code)
        else:
            print("Crawl product: ", product_id,
                  "failed : ", response.status_code)

    return product_detail_list


def save_raw_product(product_detail_list=[]):
    file = open(product_raw_data_file, "w+")
    file.write("\n".join(product_detail_list))
    file.close()
    print("Save file: ", product_raw_data_file)


def load_raw_product():
    file = open(product_raw_data_file, "r")
    return file.readlines()


flatten_field = ["badges", "inventory", "url_attendant_input_form", "salable_type", "categories",
                 "rating_summary", "data_version", "meta_title", "meta_description", "liked",
                 "brand", "seller_specifications", "other_sellers", "configurable_options",
                 "configurable_products", "product_links", "is_seller_in_chat_whitelist",
                 "youtube", "services_and_promotions", "promotions", "installment_info"]


def adjust_product(product):
    e = json.loads(product)
    if not e.get("id", False):
        return None

    for field in flatten_field:
        if field in e:
            e[field] = json.dumps(
                e[field], ensure_ascii=False)

    return e


def save_product_list(adjsust_product_list):
    file = open(product_file, "w", encoding="utf-8")
    csv_writer = csv.writer(file)

    count = 0
    for p in adjsust_product_list:

        if p is not None:
            if count == 0:
                header = p.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(p.values())
    file.close()
    print("Save file: ", product_file)


# crawl product id
product_ids, page = crawl_product_id()

print("No. Page: ", page)
print("Total Products: ", len(product_ids))

# save product ids for backup
save_product_id(product_ids)

# product_ids = load_product_ids()
# crawl detail for each product id
product_list = crawl_product(product_ids)

# # save product detail for backup
save_raw_product(product_list)

# product_list = load_raw_product()
# # flatten detail before converting to csv
# adjsust_product_list = [adjust_product(p) for p in product_list]
# # save product to csv
# save_product_list(adjsust_product_list)
