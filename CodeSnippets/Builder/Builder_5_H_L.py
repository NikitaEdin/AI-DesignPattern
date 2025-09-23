class ComplexNumberBuilder:
    def __init__(self):
        self.real = 0
        self.imag = 0

    def set_real(self, real):
        self.real = real
        return self

    def set_imag(self, imag):
        self.imag = imag
        return self

    def build(self):
        return ComplexNumber(self.real, self.imag)

class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def add(self, other):
        return ComplexNumberBuilder() \
            .set_real(self.real + other.real) \
            .set_imag(self.imag + other.imag) \
            .build()

    def subtract(self, other):
        return ComplexNumberBuilder() \
            .set_real(self.real - other.real) \
            .set_imag(self.imag - other.imag) \
            .build()

    def multiply(self, other):
        real = self.real * other.real
        imag = self.imag * other.imag
        return ComplexNumberBuilder() \
            .set_real(real - imag) \
            .set_imag(real + imag) \
            .build()

    def divide(self, other):
        real = (self.real * other.real + self.imag * other.imag) / (other.real ** 2 + other.imag ** 2)
        imag = (self.imag * other.real - self.real * other.imag) / (other.real ** 2 + other.imag ** 2)
        return ComplexNumberBuilder() \
            .set_real(real) \
            .set_imag(imag) \
            .build()

if __name__ == "__main__":
    complex1 = ComplexNumberBuilder() \
        .set_real(3) \
        .set_imag(4) \
        .build()

    complex2 = ComplexNumberBuilder() \
        .set_real(5) \
        .set_imag(-6) \
        .build()

    print("Complex1:", complex1.real, "+", complex1.imag, "i")
    print("Complex2:", complex2.real, "+", complex2.imag, "i")
    print("Addition:", complex1.add(complex2))
    print("Subtraction:", complex1.subtract(complex2))
    print("Multiplication:", complex1.multiply(complex2))
    print("Division:", complex1.divide(complex2))