import csv
import json
import requests

book_page_url = "https://tiki.vn/api/v2/products?category=320&urlKey=business-economics&limit=300&page={}"
product_url = "https://tiki.vn/api/v2/products/{}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
book_ids_file = "./book-id.txt"
book_data_file = "./book.txt"
product_file = "./product-file.csv"


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, indent=4)
    print(text)


def crawl_product_id():
    book_ids = []
    i = 0
    page = 1
    while (True):
        print("Crawl page: ", page)

        response = requests.get(book_page_url.format(page), headers=headers)

        books = response.json()['data']

        if (len(books) == 0):
            # if(page == 2):
            print('No more data !!! End here.')
            break

        for book in books:
            book_ids.append(str(book['id']))

        print("No. Books ID: ", len(book_ids))

        i += 1
        page += 1
    return book_ids, i


def save_product_id(book_ids=[]):
    file = open(book_ids_file, "w+")
    file.write('\n'.join(book_ids))
    file.close()
    print("Save file: ", book_ids_file)


def crawl_product(book_ids=[]):
    book_detail_list = []
    for book_id in book_ids:
        response = requests.get(product_url.format(book_id), headers=headers)

        if (response.status_code == 200):
            book_detail_list.append(response.text)
            print("Crawl product: ", book_id,
                  ": ", response.status_code)
        else:
            print("{'\033[93m'}Crawl product: ", book_id,
                  "failed : ", response.status_code)
            break
    return book_detail_list


def save_raw_product(product_detail_list=[]):
    file = open(book_data_file, "w+")
    file.write("\n".join(product_detail_list))
    file.close()
    print("Save file: ", book_data_file)


def load_raw_product():
    file = open(book_data_file, "r")
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
                e[field], ensure_ascii=False).replace('\n', '')

    return e


def save_product_list(adjsust_product_list):
    file = open(product_file, "w")
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


# crawl book id
book_ids, page = crawl_product_id()

print("No. Page: ", page)
print("Total Books: ", len(book_ids))

# save book ids for backup
save_product_id(book_ids)

# crawl detail for each product id
product_list = crawl_product(book_ids)

# save product detail for backup
save_raw_product(product_list)

# product_list = load_raw_product()
# # flatten detail before converting to csv
# adjsust_product_list = [adjust_product(p) for p in product_list]
# # save product to csv
# save_product_list(adjsust_product_list)
