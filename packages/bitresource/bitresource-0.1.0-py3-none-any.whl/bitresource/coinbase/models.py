from http_resource.utils import APIObject


class AddressObject(APIObject): pass


class PaymentMethodObject(APIObject): pass


class AccountObject(APIObject):
    def get_addresses(self, **params):
        """https://developers.coinbase.com/api/v2#list-addresses"""
        return self.api_client.query(*(self.api_client.urls + (self.id, 'addresses')), api_object=AddressObject,
                                     **params)
