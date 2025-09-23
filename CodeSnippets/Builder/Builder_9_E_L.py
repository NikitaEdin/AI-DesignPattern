class AddressBuilder:
    def __init__(self):
        self.address = {}

    def set_street(self, street):
        self.address['street'] = street
        return self

    def set_city(self, city):
        self.address['city'] = city
        return self

    def set_state(self, state):
        self.address['state'] = state
        return self

    def set_zipcode(self, zipcode):
        self.address['zipcode'] = zipcode
        return self

    def build(self):
        return self.address

# Usage example
if __name__ == "__main__":
    address = AddressBuilder() \
            .set_street('123 Main St') \
            .set_city('Anytown') \
            .set_state('CA') \
            .set_zipcode(12345) \
            .build()

    print(address) # Output: {'street': '123 Main St', 'city': 'Anytown', 'state': 'CA', 'zipcode': 12345}