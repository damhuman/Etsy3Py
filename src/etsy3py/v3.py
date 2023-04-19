from typing import Optional, Type, List

import requests

from src.etsy3py.base_client import BaseApiClient


class EtsyApi(BaseApiClient):
    def __init__(self, access_token: str, token_type: Optional[str] = 'Bearer',
                 auth_header: Optional[str] = 'x-api-key') -> None:
        self.__token = access_token
        self.__token_type = token_type
        self.__auth_header = auth_header

    def get_shop_receipt(self, shop_id: int, receipt_id: int) -> Type[requests.Response]:
        """
        Retrieves a receipt, identified by a receipt id, from an Etsy shop
        https://developers.etsy.com/documentation/reference/#operation/getShopReceipt
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param receipt_id: int - the numeric ID for the receipt associated to this transaction
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}"
        r = self._get(path=path, auth_type='token')
        return r

    def update_shop_receipt(self, shop_id: int, receipt_id: int,
                            was_shipped: Optional[bool] = None,
                            was_paid: Optional[bool] = None) -> Type[requests.Response]:
        """
        Updates the status of a receipt, identified by a receipt id, from an Etsy shop
        https://developers.etsy.com/documentation/reference/#operation/updateShopReceipt
        Scopes: 'transactions_w'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param receipt_id: int - the numeric ID for the receipt associated to this transaction
        :param was_shipped: Optional[bool] - default: None, when true, returns receipts where the seller shipped the product(s) in this receipt. When false, returns receipts where shipment has not been set
        :param was_paid: Optional[bool] - default: None, when true, returns receipts where the seller has received payment for the receipt. When false, returns receipts where payment has not been received
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}"
        data = {"was_shipped": was_shipped, "was_paid": was_paid}
        r = self._put(path=path, data=data, auth_type='token')
        return r

    def get_shop_receipts(self, shop_id: int,
                          min_created: Optional[int] = None,
                          max_created: Optional[int] = None,
                          min_last_modified: Optional[int] = None,
                          max_last_modified: Optional[int] = None,
                          limit: Optional[int] = None,
                          offset: Optional[int] = None,
                          sort_on: Optional[str] = None,
                          sort_order: Optional[str] = None,
                          was_paid: Optional[bool] = None,
                          was_shipped: Optional[bool] = None,
                          was_delivered: Optional[bool] = None) -> Type[requests.Response]:
        """
        Requests the Shop Receipts from a specific Shop, unfiltered or filtered by receipt id range or offset, date,
        paid, and/or shipped purchases.
        https://developers.etsy.com/documentation/reference/#operation/getShopReceipts
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param min_created: int - default: None, the earliest unix timestamp for when a record was created
        :param max_created: int - default: None, the latest unix timestamp for when a record was created
        :param min_last_modified: int - default: None, the earliest unix timestamp for when a record last changed
        :param max_last_modified: int - default: None, the latest unix timestamp for when a record last changed
        :param limit: int [1 .. 100] - default: 25, the maximum number of results to return
        :param offset: int - default: 0, the number of records to skip before selecting the first result
        :param sort_on: str Enum["created", "updated", "receipt_id"] - default: "created", the value to sort a search result of listings on
        :param sort_order: str Enum["asc", "ascending", "desc", "descending", "up", "down"] - default: "desc", the ascending(up) or descending(down) order to sort receipts by
        :param was_paid: bool - when true, returns receipts where the seller has received payment for the receipt. When false, returns receipts where payment has not been received
        :param was_shipped: bool - when true, returns receipts where the seller shipped the product(s) in this receipt. When false, returns receipts where shipment has not been set
        :param was_delivered: bool - when true, returns receipts that have been marked as delivered. When false, returns receipts where shipment has not been marked as delivered
        :return: requests.Response
        """

        path = f"/v3/application/shops/{shop_id}/receipts"
        params = {
            "min_created": min_created,
            "max_created": max_created,
            "min_last_modified": min_last_modified,
            "max_last_modified": max_last_modified,
            "limit": limit,
            "offset": offset,
            "sort_on": sort_on,
            "sort_order": sort_order,
            "was_paid": was_paid,
            "was_shipped": was_shipped,
            "was_delivered": was_delivered
        }
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def create_receipt_shipment(self, shop_id: int, receipt_id: int,
                                tracking_code: str, carrier_name: str,
                                send_bcc: bool, note_to_buyer: str) -> Type[requests.Response]:
        """
        Submits tracking information for a Shop Receipt, which creates a Shop Receipt Shipment entry for the given
        receipt_id. Each time you successfully submit tracking info, Etsy sends a notification email to the buyer User.
        When send_bcc is true, Etsy sends shipping notifications to the seller as well. When tracking_code and
        carrier_name aren't sent, the receipt is marked as shipped only. If the carrier is not supported, you may use
        other as the carrier name, so you can provide the tracking code.
        **NOTE** When shipping within the United States AND the order is over $10 or when shipping to India, tracking
        code and carrier name ARE required.
        https://developers.etsy.com/documentation/reference/#operation/createReceiptShipment
        Scopes: 'transactions_w'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param receipt_id: int - the receipt to submit tracking for
        :param tracking_code: str - the tracking code for this receipt
        :param carrier_name: str - the carrier name for this receipt
        :param send_bcc: bool - if true, the shipping notification will be sent to the seller as well
        :param note_to_buyer: str - message to include in notification to the buyer
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}/tracking"
        data = {
            "tracking_code": tracking_code,
            "carrier_name": carrier_name,
            "send_bcc": send_bcc,
            "note_to_buyer": note_to_buyer
        }
        r = self._post(path=path, data=data, auth_type='token')
        return r

    def get_shop_receipt_transactions_by_listing(self, shop_id: int, listing_id: int,
                                                 limit: Optional[int] = None,
                                                 offset: Optional[int] = None) -> Type[requests.Response]:
        """
        Retrieves the list of transactions associated with a listing.
        https://developers.etsy.com/documentation/reference/#operation/getShopReceiptTransactionsByListing
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :param limit: int [1 .. 100] - default: 25, the maximum number of results to return
        :param offset: int - default: 0, the number of records to skip before selecting the first result
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings/{listing_id}/transactions"
        params = {
            "limit": limit,
            "offset": offset
        }
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def get_shop_receipt_transactions_by_receipt(self, shop_id: int, receipt_id: int) -> Type[requests.Response]:
        """
        Retrieves the list of transactions associated with a specific receipt.
        https://developers.etsy.com/documentation/reference/#operation/getShopReceiptTransactionsByReceipt
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param receipt_id: int - the numeric ID for the receipt associated to this transaction
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}/transactions"
        r = self._get(path=path, auth_type='token')
        return r

    def get_shop_receipt_transaction(self, shop_id: int, transaction_id: int) -> Type[requests.Response]:
        """
        Retrieves a transaction by transaction ID.
        https://developers.etsy.com/documentation/reference/#operation/getShopReceiptTransaction
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param transaction_id: int - the unique numeric ID for a transaction
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/transactions/{transaction_id}"
        r = self._get(path=path, auth_type='token')
        return r

    def get_shop_receipt_transactions_by_shop(self, shop_id: int,
                                              limit: Optional[int] = None,
                                              offset: Optional[int] = None) -> Type[requests.Response]:
        """
        Retrieves the list of transactions associated with a shop.
        https://developers.etsy.com/documentation/reference/#operation/getShopReceiptTransactionsByShop
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param limit: int [1 .. 100] - default: 25, the maximum number of results to return
        :param offset: int - default: 0, the number of records to skip before selecting the first result
        :return: requests.Response
        """
        path = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/transactions"
        params = {
            "limit": limit,
            "offset": offset
        }
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def get_listing_inventory(self, listing_id: int, includes: Optional[str] = None,
                              show_deleted: bool = False) -> Type[requests.Response]:
        """
        Retrieves the inventory record for a listing. Listings you did not edit using the Etsy.com inventory tools have
        no inventory records. This endpoint returns SKU data if you are the owner of the inventory records being
        fetched.
        https://developers.etsy.com/documentation/reference/#operation/getListingInventory
        Scopes: 'listings_r'

        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :param includes: str Enum["Listing"] - default: None, an enumerated string that attaches a valid association
        :param show_deleted: bool - default: False, a boolean value for inventory whether to include deleted products and their offerings
        :return: requests.Response
        """
        path = f"https://openapi.etsy.com/v3/application/listings/{listing_id}/inventory"
        params = {
            "includes": includes,
            "show_deleted": show_deleted
        }
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def update_listing_inventory(self, listing_id: int, products: List[dict],
                                 price_on_property: List[int], quantity_on_property: List[int],
                                 sku_on_property: List[int]) -> Type[requests.Response]:
        """
        Updates the inventory for a listing identified by a listing ID. The update fails if the supplied values for
        product sku, offering quantity, and/or price are incompatible with values in *_on_property_* fields.
        When setting a price, assign a float equal to amount divided by divisor as specified in the Money resource.
        https://developers.etsy.com/documentation/reference/#operation/updateListingInventory
        Scopes: 'listings_w'

        "products": [
            {
              "sku": "string",
              "property_values": [
                {
                  "property_id": 1,
                  "value_ids": [
                    1
                  ],
                  "scale_id": 1,
                  "property_name": "string",
                  "values": [
                    "string"
                  ]
                }
              ],
              "offerings": [
                {
                  "price": 0,
                  "quantity": 0,
                  "is_enabled": true
                }
              ]
            }
        ]

        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :param products: List[dict] - a JSON array of products available in a listing, even if only one product. All field names in the JSON blobs are lowercase
        :param price_on_property: List[int] - an array of unique listing property ID integers for the properties that change product prices, if any. For example, if you charge specific prices for different sized products in the same listing, then this array contains the property ID for size
        :param quantity_on_property: List[int] - an array of unique listing property ID integers for the properties that change the quantity of the products, if any. For example, if you stock specific quantities of different colored products in the same listing, then this array contains the property ID for color
        :param sku_on_property: List[int] - an array of unique listing property ID integers for the properties that change the product SKU, if any. For example, if you use specific skus for different colored products in the same listing, then this array contains the property ID for color.
        :return: requests.Response
        """
        path = f"/v3/application/listings/{listing_id}/inventory"
        data = {
            "products": products,
            "price_on_property": price_on_property,
            "quantity_on_property": quantity_on_property,
            "sku_on_property": sku_on_property
        }
        r = self._put(path=path, data=data, auth_type='token')
        return r
