class Computer:
    def __init__(self):
        self.components = {}

    def add_component(self, name, component):
        self.components[name] = component

    def __str__(self):
        return f"Computer components: {self.components}"

class PCConfigurator:
    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu):
        if not cpu:
            raise ValueError("CPU cannot be empty")
        self.computer.add_component("CPU", cpu)
        return self

    def set_ram(self, ram):
        if not ram:
            raise ValueError("RAM cannot be empty")
        self.computer.add_component("RAM", ram)
        return self

    def set_hdd(self, hdd):
        if not hdd:
            raise ValueError("HDD cannot be empty")
        self.computer.add_component("HDD", hdd)
        return self

    def get_computer(self):
        essential = ["CPU", "RAM", "HDD"]
        if not all(comp in self.computer.components for comp in essential):
            raise ValueError("Computer must include CPU, RAM, and HDD")
        return self.computer

class ComputerDirector:
    def __init__(self, configurator):
        self.configurator = configurator

    def construct_gaming_pc(self):
        self.configurator.set_cpu("Intel i7").set_ram("16GB").set_hdd("1TB SSD")

    def construct_office_pc(self):
        self.configurator.set_cpu("Intel i3").set_ram("8GB").set_hdd("500GB HDD")

if __name__ == "__main__":
    try:
        config = PCConfigurator()
        director = ComputerDirector(config)
        director.construct_gaming_pc()
        gaming_pc = config.get_computer()
        print(gaming_pc)
    except ValueError as e:
        print(f"Error: {e}")

    try:
        config2 = PCConfigurator()
        director2 = ComputerDirector(config2)
        director2.construct_office_pc()
        office_pc = config2.get_computer()
        print(office_pc)
    except ValueError as e:
        print(f"Error: {e}")