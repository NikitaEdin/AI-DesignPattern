class MealBuilder:
    def __init__(self):
        self.meal = []

    def add_ingredient(self, ingredient):
        self.meal.append(ingredient)

    def build(self):
        return self.meal

class VeggieMealBuilder:
    def __init__(self):
        self.meal = []

    def add_veggie(self, veggie):
        self.meal.append(veggie)

    def build(self):
        return self.meal

class MealDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct_meal(self):
        self.builder.add_ingredient('bread')
        self.builder.add_veggie('broccoli')
        return self.builder.build()

# Usage example
def main():
    veggie_meal = VeggieMealBuilder()
    meal_director = MealDirector(veggie_meal)
    meal = meal_director.construct_meal()
    print(meal)

if __name__ == "__main__":
    main()