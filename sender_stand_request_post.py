import configuration
import requests
import data


# def post_products_kits(id):
#     return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
#                          json=id,
#                          headers=data.headers)
#
#
# response = post_products_kits(data.product_ids);
# print(response.status_code)
# print(response.json())

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # подставляем полный url
                         json=body,  # тут тело
                         headers=data.headers)  # а здесь заголовки


response = post_new_user(data.user_body);
print(response.status_code)
