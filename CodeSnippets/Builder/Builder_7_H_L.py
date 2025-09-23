[/PYTHON]

[EXPLANATION]
The Builder design pattern is used to create objects step by step, avoiding the need for complex constructors or factories. In this example, we define a `DocumentBuilder` class that provides methods for setting various properties of a document, such as its title, author, and body. The builder pattern allows us to create documents in a more flexible and modular way, since it separates the process of creating objects from their actual implementation.

In this code snippet, we define a `main` function that demonstrates how to use the `DocumentBuilder` class. We first create an instance of the `DocumentBuilder` class using the `with_title`, `with_author`, and `with_body` methods. These methods return `self`, which allows us to chain calls to these methods together. Once we have set all the properties of the document, we call the `build` method to create the final object.

The `DocumentBuilder` class is a good example of the Builder pattern because it provides a flexible way to create objects by allowing users to set properties in any order and using methods to validate and transform input data. By separating the process of creating objects from their implementation, we can avoid complex constructors or factories and make our code more modular and maintainable.
[/EXPLANATION]

[PYTHON]
class DocumentBuilder:
    def __init__(self):
        self.title = None
        self.author = None
        self.body = []

    def with_title(self, title):
        self.title = title
        return self

    def with_author(self, author):
        self.author = author
        return self

    def with_body(self, body):
        self.body.append(body)
        return self

    def build(self):
        return {
            'title': self.title,
            'author': self.author,
            'body': self.body
        }

def main():
    document_builder = DocumentBuilder() \
                          .with_title("The Great Gatsby") \
                          .with_author("F. Scott Fitzgerald") \
                          .with_body("This is the first paragraph.") \
                          .with_body("This is the second paragraph.") \
                          .build()
    print(document_builder)

if __name__ == "__main__":
    main()