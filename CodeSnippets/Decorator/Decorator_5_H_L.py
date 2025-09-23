def make_bold(fn):
    def wrapper():
        return f"<b>{fn()}</b>"
    return wrapper

@make_bold
def get_html():
    return "Hello, world!"

if __name__ == "__main__":
    print(get_html())