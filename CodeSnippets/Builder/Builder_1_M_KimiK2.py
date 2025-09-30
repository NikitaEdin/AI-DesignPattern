import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class Espresso:
    def __init__(self, bean_type, grind_size, water_temp, brew_time):
        self.bean_type = bean_type
        self.grind_size = grind_size
        self.water_temp = water_temp
        self.brew_time = brew_time

    def __repr__(self):
        return (f"Espresso({self.bean_type}, {self.grind_size}μm, "
                f"{self.water_temp}°C, {self.brew_time}s)")


class EspressoCraftsman:
    def __init__(self):
        self.bean_type = None
        self.grind_size = None
        self.water_temp = None
        self.brew_time = None
        self.built = False

    def select_beans(self, bean_type):
        if self.built:
            raise ValueError("Already prepared")
        self.bean_type = bean_type
        logger.info("Beans selected: %s", bean_type)
        return self

    def set_grind_size(self, grind_size):
        if self.built:
            raise ValueError("Already prepared")
        self.grind_size = grind_size
        logger.info("Grind size set: %s μm", grind_size)
        return self

    def set_water_temperature(self, water_temp):
        if self.built:
            raise ValueError("Already prepared")
        self.water_temp = water_temp
        logger.info("Water temperature set: %s °C", water_temp)
        return self

    def set_brew_time(self, brew_time):
        if self.built:
            raise ValueError("Already prepared")
        self.brew_time = brew_time
        logger.info("Brew time set: %s s", brew_time)
        return self

    def prepare(self):
        if self.built:
            raise ValueError("Already prepared")
        for attr in (self.bean_type, self.grind_size, self.water_temp,
                     self.brew_time):
            if attr is None:
                raise ValueError("All parameters must be specified")
        self.built = True
        logger.info("Espresso prepared successfully")
        return Espresso(self.bean_type, self.grind_size, self.water_temp,
                        self.brew_time)


if __name__ == "__main__":
    drink = (EspressoCraftsman()
             .select_beans("Arabica")
             .set_grind_size(200)
             .set_water_temperature(92)
             .set_brew_time(28)
             .prepare())
    print(drink)