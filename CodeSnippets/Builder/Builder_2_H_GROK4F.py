class Meal:
    def __init__(self):
        self.appetizer = ""
        self.main_course = ""
        self.dessert = ""
        self.drink = ""
        self.price = 0.0

    def display(self):
        print("=== Your Meal ===")
        if self.appetizer:
            print(f"Appetizer: {self.appetizer}")
        if self.main_course:
            print(f"Main Course: {self.main_course}")
        if self.dessert:
            print(f"Dessert: {self.dessert}")
        if self.drink:
            print(f"Drink: {self.drink}")
        if not any([self.appetizer, self.main_course, self.dessert, self.drink]):
            print("No items in meal.")
        print(f"Total Price: ${self.price:.2f}\n")

class MealPreparer:
    def __init__(self):
        self._meal = Meal()

    def build_appetizer(self):
        pass

    def build_main_course(self):
        pass

    def build_dessert(self):
        pass

    def build_drink(self):
        pass

    def get_meal(self):
        if not self._meal.main_course:
            raise ValueError("A main course must be specified for the meal.")
        return self._meal

    def reset(self):
        self._meal = Meal()
        return self

class VegetarianMealPreparer(MealPreparer):
    def build_appetizer(self):
        self._meal.appetizer = "Garden Salad"
        self._meal.price += 5.0

    def build_main_course(self):
        self._meal.main_course = "Veggie Pasta"
        self._meal.price += 12.0

    def build_dessert(self):
        self._meal.dessert = "Fruit Platter"
        self._meal.price += 4.0

    def build_drink(self):
        self._meal.drink = "Lemonade"
        self._meal.price += 2.0

class NonVegetarianMealPreparer(MealPreparer):
    def build_appetizer(self):
        self._meal.appetizer = "Chicken Soup"
        self._meal.price += 6.0

    def build_main_course(self):
        self._meal.main_course = "Grilled Chicken"
        self._meal.price += 15.0

    def build_dessert(self):
        self._meal.dessert = "Ice Cream"
        self._meal.price += 3.0

    def build_drink(self):
        self._meal.drink = "Soda"
        self._meal.price += 2.0

class MealDirector:
    def construct_full_meal(self, preparer):
        preparer.build_appetizer()
        preparer.build_main_course()
        preparer.build_dessert()
        preparer.build_drink()

    def construct_basic_meal(self, preparer):
        preparer.build_appetizer()
        preparer.build_main_course()
        preparer.build_drink()

if __name__ == "__main__":
    director = MealDirector()
    veg_preparer = VegetarianMealPreparer()
    director.construct_full_meal(veg_preparer)
    full_veg_meal = veg_preparer.get_meal()
    full_veg_meal.display()

    veg_preparer.reset()
    director.construct_basic_meal(veg_preparer)
    basic_veg_meal = veg_preparer.get_meal()
    basic_veg_meal.display()

    nonveg_preparer = NonVegetarianMealPreparer()
    director.construct_full_meal(nonveg_preparer)
    full_nonveg_meal = nonveg_preparer.get_meal()
    full_nonveg_meal.display()