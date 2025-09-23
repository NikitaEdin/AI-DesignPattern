class Meal:
    def __init__(self):
        self.main_course = None
        self.dessert = None
        self.drink = None

    def __str__(self):
        return f"Meal with {self.main_course}, {self.dessert}, and {self.drink}"

class MealPreparer:
    def __init__(self):
        self.meal = Meal()

    def set_main_course(self, course):
        self.meal.main_course = course
        return self

    def set_dessert(self, dessert):
        self.meal.dessert = dessert
        return self

    def set_drink(self, drink):
        self.meal.drink = drink
        return self

    def create(self):
        if not self.meal.main_course:
            raise ValueError("A main course must be selected.")
        return self.meal

class Chef:
    def __init__(self, preparer):
        self.preparer = preparer

    def prepare_vegetarian_option(self):
        return (self.preparer
                .set_main_course("Grilled Vegetables")
                .set_dessert("Fruit Salad")
                .set_drink("Lemonade")
                .create())

    def prepare_meat_option(self):
        return (self.preparer
                .set_main_course("Steak")
                .set_dessert("Cheesecake")
                .set_drink("Cola")
                .create())

if __name__ == "__main__":
    preparer = MealPreparer()
    chef = Chef(preparer)
    vegetarian_meal = chef.prepare_vegetarian_option()
    print(vegetarian_meal)
    meat_meal = chef.prepare_meat_option()
    print(meat_meal)