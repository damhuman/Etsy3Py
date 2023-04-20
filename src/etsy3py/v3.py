from typing import Optional, List

import requests

from src.etsy3py.base_client import BaseApiClient


class EtsyApi(BaseApiClient):
    def __init__(self, access_token: str, client_id: str, token_type: Optional[str] = 'Bearer') -> None:
        """
        Initialize EtsyApi.
        :param access_token: str - user access token
        :param client_id: str - client id, from ETSY developer platform
        :param token_type: str - default: bearer, token type
        """
        super().__init__(access_token, client_id, token_type)

    def get_me(self) -> requests.Response:
        """
        Returns basic info for the user making the request.
        https://developers.etsy.com/documentation/reference#operation/getMe
        Scopes: 'shops_r'

        :return: requests.Response
        """
        path = f"/v3/application/users/me"
        r = self._get(path=path, auth_type='token')
        return r

    def get_shop_receipt(self, shop_id: int, receipt_id: int) -> requests.Response:
        """
        Retrieves a receipt, identified by a receipt id, from an Etsy shop.
        https://developers.etsy.com/documentation/reference/#operation/getShopReceipt
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param receipt_id: int - the numeric ID for the receipt associated to this transaction
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}"
        r = self._get(path=path, auth_type='token')
        return r

    def update_shop_receipt(self, shop_id: int, receipt_id: int, **kwargs) -> requests.Response:
        """
        Updates the status of a receipt, identified by a receipt id, from an Etsy shop.
        https://developers.etsy.com/documentation/reference/#operation/updateShopReceipt
        Scopes: 'transactions_w'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param receipt_id: int - the numeric ID for the receipt associated to this transaction
        :key was_shipped: Optional[bool] - default: None, when true, returns receipts where the seller shipped the product(s) in this receipt. When false, returns receipts where shipment has not been set
        :key was_paid: Optional[bool] - default: None, when true, returns receipts where the seller has received payment for the receipt. When false, returns receipts where payment has not been received
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}"
        data = {**kwargs}
        r = self._put(path=path, data=data, auth_type='token')
        return r

    def get_shop_receipts(self, shop_id: int, **kwargs) -> requests.Response:
        """
        Requests the Shop Receipts from a specific Shop, unfiltered or filtered by receipt id range or offset, date,
        paid, and/or shipped purchases.
        https://developers.etsy.com/documentation/reference/#operation/getShopReceipts
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :key min_created: int - default: None, the earliest unix timestamp for when a record was created
        :key max_created: int - default: None, the latest unix timestamp for when a record was created
        :key min_last_modified: int - default: None, the earliest unix timestamp for when a record last changed
        :key max_last_modified: int - default: None, the latest unix timestamp for when a record last changed
        :key limit: int [1 .. 100] - default: 25, the maximum number of results to return
        :key offset: int - default: 0, the number of records to skip before selecting the first result
        :key sort_on: str Enum["created", "updated", "receipt_id"] - default: "created", the value to sort a search result of listings on
        :key sort_order: str Enum["asc", "ascending", "desc", "descending", "up", "down"] - default: "desc", the ascending(up) or descending(down) order to sort receipts by
        :key was_paid: bool - when true, returns receipts where the seller has received payment for the receipt. When false, returns receipts where payment has not been received
        :key was_shipped: bool - when true, returns receipts where the seller shipped the product(s) in this receipt. When false, returns receipts where shipment has not been set
        :key was_delivered: bool - when true, returns receipts that have been marked as delivered. When false, returns receipts where shipment has not been marked as delivered
        :return: requests.Response
        """

        path = f"/v3/application/shops/{shop_id}/receipts"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def create_receipt_shipment(self, shop_id: int, receipt_id: int, **kwargs) -> requests.Response:
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
        :key tracking_code: str - the tracking code for this receipt
        :key carrier_name: str - the carrier name for this receipt
        :key send_bcc: bool - if true, the shipping notification will be sent to the seller as well
        :key note_to_buyer: str - message to include in notification to the buyer
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}/tracking"
        data = {**kwargs}
        r = self._post(path=path, data=data, auth_type='token')
        return r

    def get_shop_receipt_transactions_by_listing(self, shop_id: int, listing_id: int, **kwargs) -> requests.Response:
        """
        Retrieves the list of transactions associated with a listing.
        https://developers.etsy.com/documentation/reference/#operation/getShopReceiptTransactionsByListing
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :key limit: int [1 .. 100] - default: 25, the maximum number of results to return
        :key offset: int - default: 0, the number of records to skip before selecting the first result
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings/{listing_id}/transactions"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def get_shop_receipt_transactions_by_receipt(self, shop_id: int, receipt_id: int) -> requests.Response:
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

    def get_shop_receipt_transaction(self, shop_id: int, transaction_id: int) -> requests.Response:
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

    def get_shop_receipt_transactions_by_shop(self, shop_id: int, **kwargs) -> requests.Response:
        """
        Retrieves the list of transactions associated with a shop.
        https://developers.etsy.com/documentation/reference/#operation/getShopReceiptTransactionsByShop
        Scopes: 'transactions_r'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :key limit: int [1 .. 100] - default: 25, the maximum number of results to return
        :key offset: int - default: 0, the number of records to skip before selecting the first result
        :return: requests.Response
        """
        path = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/transactions"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def get_listing_inventory(self, listing_id: int, **kwargs) -> requests.Response:
        """
        Retrieves the inventory record for a listing. Listings you did not edit using the Etsy.com inventory tools have
        no inventory records. This endpoint returns SKU data if you are the owner of the inventory records being
        fetched.
        https://developers.etsy.com/documentation/reference/#operation/getListingInventory
        Scopes: 'listings_r'

        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :key includes: str Enum["Listing"] - default: None, an enumerated string that attaches a valid association
        :key show_deleted: bool - default: False, a boolean value for inventory whether to include deleted products and their offerings
        :return: requests.Response
        """
        path = f"https://openapi.etsy.com/v3/application/listings/{listing_id}/inventory"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def update_listing_inventory(self, listing_id: int, products: List[dict], **kwargs) -> requests.Response:
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
        :key price_on_property: List[int] - an array of unique listing property ID integers for the properties that change product prices, if any. For example, if you charge specific prices for different sized products in the same listing, then this array contains the property ID for size
        :key quantity_on_property: List[int] - an array of unique listing property ID integers for the properties that change the quantity of the products, if any. For example, if you stock specific quantities of different colored products in the same listing, then this array contains the property ID for color
        :key sku_on_property: List[int] - an array of unique listing property ID integers for the properties that change the product SKU, if any. For example, if you use specific skus for different colored products in the same listing, then this array contains the property ID for color.
        :return: requests.Response
        """
        path = f"/v3/application/listings/{listing_id}/inventory"
        data = {
            "products": products,
            **kwargs
        }
        r = self._put(path=path, data=data, auth_type='token')
        return r

    def create_draft_listing(self, shop_id: int, **kwargs) -> requests.Response:
        """
        Creates a physical draft listing product in a shop on the Etsy channel.
        https://developers.etsy.com/documentation/reference#operation/createDraftListing
        Scopes: 'listings_w'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings"
        data = {**kwargs}
        r = self._post(path=path, data=data, auth_type='token')
        return r

    def get_listings_by_shop(self, shop_id: int, **kwargs) -> requests.Response:
        """
        Endpoint to list Listings that belong to a Shop. Listings can be filtered using the 'state' param.
        https://developers.etsy.com/documentation/reference#operation/getListingsByShop
        Scopes: 'listings_r'

        :param shop_id:  int - the unique positive non-zero numeric ID for an Etsy Shop
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def delete_listing(self, listing_id: int) -> requests.Response:
        """
        Open API V3 endpoint to delete a ShopListing. A ShopListing can be deleted only if the state is one of the
        following: SOLD_OUT, DRAFT, EXPIRED, INACTIVE, ACTIVE and is_available or ACTIVE and has seller flags:
        SUPPRESSED (frozen), VACATION, CUSTOM_SHOPS (pattern), SELL_ON_FACEBOOK.
        https://developers.etsy.com/documentation/reference#operation/deleteListing
        Scopes: 'listings_d'

        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :return: requests.Response
        """
        path = f"/v3/application/listings/{listing_id}"
        r = self._delete(path=path, auth_type='token')
        return r

    def get_listing(self, listing_id: int, **kwargs) -> requests.Response:
        """
        Retrieves a listing record by listing ID.
        https://developers.etsy.com/documentation/reference#operation/getListing

        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :return: requests.Response
        """
        path = f"/v3/application/listings/{listing_id}"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def find_all_listings_active(self, **kwargs) -> requests.Response:
        """
        A list of all active listings on Etsy paginated by their creation date. Without sort_order listings will be
        returned newest-first by default.
        https://developers.etsy.com/documentation/reference#operation/findAllListingsActive

        :return: requests.Response
        """
        path = f"/v3/application/listings/active"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def find_all_active_listings_by_shop(self, shop_id: int, **kwargs) -> requests.Response:
        """
        Retrieves a list of all active listings on Etsy in a specific shop, paginated by listing creation date.
        https://developers.etsy.com/documentation/reference#operation/findAllActiveListingsByShop

        :param shop_id:  int - the unique positive non-zero numeric ID for an Etsy Shop
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings/active"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def get_listings_by_listing_ids(self, listing_ids: List[int], **kwargs) -> requests.Response:
        """
        Allows to query multiple listing ids at once. Limit 100 ids maximum per query.
        https://developers.etsy.com/documentation/reference#operation/getListingsByListingIds

        :param listing_ids: List[int] - the list of numeric IDS for the listings in a specific Etsy shop
        :key includes: List[str] Enum["Shipping", "Images", "Shop", "User", "Translations", "Inventory"] - default: None, an enumerated string that attaches a valid association
        :return: requests.Response
        """
        path = f"/v3/application/listings/batch"
        params = {"listing_ids": listing_ids, **kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def get_featured_listings_by_shop(self, shop_id: int, **kwargs) -> requests.Response:
        """
        Retrieves Listings associated to a Shop that are featured.
        https://developers.etsy.com/documentation/reference#operation/getFeaturedListingsByShop

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :key limit: int [1 .. 100] - default: 25, the maximum number of results to return
        :key offset: int - default: 0, the number of records to skip before selecting the first result
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings/featured"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def delete_listing_property(self, shop_id: int, listing_id: int, property_id: int) -> requests.Response:
        """
        Deletes a property for a Listing.
        https://developers.etsy.com/documentation/reference#operation/deleteListingProperty
        Scopes: 'listings_w'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :param property_id: int - the unique ID of an Etsy listing property
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings/{listing_id}/properties/{property_id}"
        r = self._delete(path=path, auth_type='token')
        return r

    def update_listing_property(self, shop_id: int, listing_id: int, property_id: int,
                                value_ids: List[int], values: List[str], **kwargs) -> requests.Response:
        """
        Updates or populates the properties list defining product offerings for a listing.
        Each offering requires both a `value` and a `value_id` that are valid for a `scale_id` assigned to the listing
        or that you assign to the listing with this request.
        https://developers.etsy.com/documentation/reference#operation/updateListingProperty
        Scopes: 'listings_w'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :param property_id: int - the unique ID of an Etsy listing property
        :param value_ids: List[int] - an array of unique IDs of multiple Etsy listing property values. For example, if your listing offers different sizes of a product, then the value ID list contains value IDs for each size
        :param values: List[str] - an array of value strings for multiple Etsy listing property values. For example, if your listing offers different colored products, then the values array contains the color strings for each color. Note: parenthesis characters (( and )) are not allowed
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings/{listing_id}/properties/{property_id}"
        data = {
            "value_ids": value_ids,
            "values": values,
            **kwargs
        }
        r = self._put(path=path, data=data, auth_type='token')
        return r

    def get_listing_property(self, listing_id: int, property_id: int) -> requests.Response:
        """
        Retrieves a listing's property.
        https://developers.etsy.com/documentation/reference#operation/getListingProperty

        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :param property_id: int - the unique ID of an Etsy listing property
        :return: requests.Response
        """
        path = f"/v3/application/listings/{listing_id}/properties/{property_id}"
        r = self._get(path=path, auth_type='token')
        return r

    def get_listing_properties(self, shop_id: int, listing_id: int) -> requests.Response:
        """
        Get a listing's properties.
        https://developers.etsy.com/documentation/reference#operation/getListingProperties

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings/{listing_id}/properties"
        r = self._get(path=path, auth_type='token')
        return r

    def update_listing(self, shop_id: int, listing_id: int, **kwargs) -> requests.Response:
        """
        Updates a listing, identified by a listing ID, for a specific shop identified by a shop ID. Note that this is a
        PATCH method type.
        https://developers.etsy.com/documentation/reference#operation/updateListing
        Scores: 'listings_w'

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/listings/{listing_id}"
        data = {**kwargs}
        r = self._patch(path=path, data=data, auth_type='token')
        return r

    def get_listings_by_shop_receipt(self, receipt_id: int, shop_id: int, **kwargs) -> requests.Response:
        """
        Gets all listings associated with a receipt.
        https://developers.etsy.com/documentation/reference#operation/getListingsByShopReceipt
        Scopes: 'transactions_r'

        :param receipt_id: int - the numeric ID for the receipt associated to this transaction
        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :key limit: int [1 .. 100] - default: 25, the maximum number of results to return
        :key offset: int - default: 0, the number of records to skip before selecting the first result
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}/listings"
        params = {**kwargs}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def get_listings_by_shop_return_policy(self, return_policy_id: int, shop_id: int) -> requests.Response:
        """
        Gets all listings associated with a Return Policy.
        https://developers.etsy.com/documentation/reference#operation/getListingsByShopReturnPolicy
        Scopes: 'listings_r'

        :param return_policy_id: int - the numeric ID of the Return Policy
        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/policies/return/{return_policy_id}/listings"
        r = self._get(path=path, auth_type='token')
        return r

    def get_listings_by_shop_section_id(self, shop_id: int, shop_section_ids: List[int], **kwargs) -> requests.Response:
        """
        Retrieves all the listings from the section of a specific shop.
        https://developers.etsy.com/documentation/reference#operation/getListingsByShopSectionId

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param shop_section_ids: List[int] - a list of numeric IDS for all sections in a specific Etsy shop
        :return: requests.Response
        """
        path = f"/v3/application/shops/{shop_id}/shop-sections/listings"
        params = {
            "shop_section_ids": shop_section_ids,
            **kwargs
        }
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def get_listing_offering(self, listing_id: int, product_id: int, product_offering_id: int) -> requests.Response:
        """
        Get an Offering for a Listing.
        https://developers.etsy.com/documentation/reference/#operation/getListingOffering

        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :param product_id: int - the numeric ID for a specific product purchased from a listing
        :param product_offering_id: int
        :return: requests.Response
        """
        path = f"/v3/application/listings/{listing_id}/products/{product_id}/offerings/{product_offering_id}"
        r = self._get(path=path, auth_type='token')
        return r

    def get_listing_product(self, listing_id: int, product_id: int) -> requests.Response:
        """
        Open API V3 endpoint to retrieve a ListingProduct by ID.
        https://developers.etsy.com/documentation/reference/#operation/getListingProduct
        Scopes: 'listings_r'

        :param listing_id: int - the numeric ID for the listing associated to this transaction
        :param product_id: int - the numeric ID for a specific product purchased from a listing
        :return: requests.Response
        """
        path = f"/v3/application/listings/{listing_id}/inventory/products/{product_id}"
        r = self._get(path=path, auth_type='token')
        return r
