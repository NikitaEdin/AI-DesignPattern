class Animal:
    """Represents an animal."""

    def __init__(self, name: str) -> None:
        self.name = name


class Dog(Animal):
    """Represents a dog."""

    def bark(self) -> None:
        print("Woof!")


class Cat(Animal):
    """Represents a cat."""

    def meow(self) -> None:
        print("Meow!")


def create_animal(name: str, sound: str) -> Animal:
    """Creates an animal based on the given name and sound.

    Args:
        name (str): The name of the animal.
        sound (str): The sound made by the animal.

    Returns:
        Animal: An instance of the animal class.
    """
    if sound == "bark":
        return Dog(name)
    elif sound == "meow":
        return Cat(name)
    else:
        raise ValueError("Invalid sound")


if __name__ == "__main__":
    # Create a dog and a cat using the factory method.
    my_dog = create_animal("Fido", "bark")
    my_cat = create_animal("Whiskers", "meow")

    # Test the created animals.
    my_dog.bark()  # Output: Woof!
    my_cat.meow()  # Output: Meow!