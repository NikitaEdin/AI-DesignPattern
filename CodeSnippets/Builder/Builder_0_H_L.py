class MealBuilder:
    def __init__(self):
        self.meal = {}
    
    def add_main_course(self, main_course):
        self.meal['main_course'] = main_course
        return self
    
    def add_side_dish(self, side_dish):
        self.meal['side_dish'] = side_dish
        return self
    
    def add_dessert(self, dessert):
        self.meal['dessert'] = dessert
        return self
    
    def build(self):
        return Meal(self.meal)
    
class Meal:
    def __init__(self, meal):
        self.main_course = meal['main_course']
        self.side_dish = meal['side_dish']
        self.dessert = meal['dessert']
    
# Usage example
if __name__ == '__main__':
    meal_builder = MealBuilder()
    main_course = MainCourse('chicken', 'roasted')
    side_dish = SideDish('mashed potatoes')
    dessert = Dessert('ice cream')
    
    meal_builder.add_main_course(main_course) \
                .add_side_dish(side_dish) \
                .add_dessert(dessert) \
                .build()