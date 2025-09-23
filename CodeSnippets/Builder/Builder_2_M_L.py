class AddressBuilder:
    def __init__(self):
        self._street = None
        self._city = None
        self._state = None
        self._zipcode = None
    
    def set_street(self, street):
        self._street = street
        return self
    
    def set_city(self, city):
        self._city = city
        return self
    
    def set_state(self, state):
        self._state = state
        return self
    
    def set_zipcode(self, zipcode):
        self._zipcode = zipcode
        return self
    
    def build(self):
        address = Address()
        address.street = self._street
        address.city = self._city
        address.state = self._state
        address.zipcode = self._zipcode
        return address

class Address:
    def __init__(self):
        self.street = None
        self.city = None
        self.state = None
        self.zipcode = None
    
if __name__ == "__main__":
    address_builder = AddressBuilder()
    address_builder.set_street("123 Main St").set_city("Anytown").set_state("CA").set_zipcode("12345")
    address = address_builder.build()
    print(address.street) # Output: 123 Main St
    print(address.city) # Output: Anytown
    print(address.state) # Output: CA
    print(address.zipcode) # Output: 12345