from typing import Optional

from src.etsy3py.base_client import BaseApiClient


class EtsyApiClient(BaseApiClient):
    def __init__(self, access_token: str):
        self.__token = access_token

    def get_shop_receipt(self, shop_id: int, receipt_id: int) -> dict:
        """
        Retrieves a receipt, identified by a receipt id, from an Etsy shop
        https://developers.etsy.com/documentation/reference/#operation/getShopReceipt

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param receipt_id: int - the numeric ID for the receipt associated to this transaction
        :return:
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}"
        r = self._get(path=path, auth_type='token')
        return r

    def update_shop_receipt(self, shop_id: int, receipt_id: int,
                            was_shipped: bool = False, was_paid: bool = False) -> dict:
        """
        Updates the status of a receipt, identified by a receipt id, from an Etsy shop
        https://developers.etsy.com/documentation/reference/#operation/updateShopReceipt

        :param shop_id: int - the unique positive non-zero numeric ID for an Etsy Shop
        :param receipt_id: int - the numeric ID for the receipt associated to this transaction
        :param was_shipped: bool - When true, returns receipts where the seller shipped the product(s) in this receipt.
        When false, returns receipts where shipment has not been set
        :param was_paid: bool - When true, returns receipts where the seller has received payment for the receipt.
        When false, returns receipts where payment has not been received
        :return:
        """
        path = f"/v3/application/shops/{shop_id}/receipts/{receipt_id}"
        params = {"was_shipped": was_shipped, "was_paid": was_paid}
        r = self._put(path=path, params=params, auth_type='token')
        return r

    def get_shop_receipts(self, shop_id: int,
                          min_created: Optional[int] = None,
                          max_created: Optional[int] = None,
                          min_last_modified: Optional[int] = None,
                          max_last_modified: Optional[int] = None,
                          limit: int = 25,
                          offset: int = 0) -> dict:
        path = f"/v3/application/shops/{shop_id}/receipts"
        params = {}
        r = self._get(path=path, params=params, auth_type='token')
        return r

    def get_listing_inventory(self, listing_id, **kwargs):
        pass

    def update_listing_inventory(self, listing_id, **kwargs):
        pass
