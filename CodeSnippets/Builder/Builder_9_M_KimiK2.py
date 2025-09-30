import re

class EmailAddress:
    def __init__(self, local_part: str, domain: str) -> None:
        self.local_part = local_part
        self.domain = domain

    def __str__(self) -> str:
        return f"{self.local_part}@{self.domain}"

class Contact:
    def __init__(self) -> None:
        self.name: str = ""
        self.phone: str = ""
        self.email: EmailAddress | None = None

    def __repr__(self) -> str:
        return f"Contact(name='{self.name}', phone='{self.phone}', email={self.email})"

class ContactAssembler:
    def __init__(self) -> None:
        self._contact = Contact()

    def set_name(self, name: str) -> "ContactAssembler":
        if not name.strip():
            raise ValueError("Name cannot be empty")
        self._contact.name = name.strip()
        return self

    def set_phone(self, phone: str) -> "ContactAssembler":
        if not re.fullmatch(r"\+\d{1,15}", phone):
            raise ValueError("Phone must be in international format: +1234567890")
        self._contact.phone = phone
        return self

    def set_email(self, local: str, domain: str) -> "ContactAssembler":
        if not re.fullmatch(r"[a-zA-Z0-9._%+-]+", local):
            raise ValueError("Invalid email local part")
        if not re.fullmatch(r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", domain):
            raise ValueError("Invalid email domain")
        self._contact.email = EmailAddress(local, domain)
        return self

    def create(self) -> Contact:
        if not self._contact.name:
            raise ValueError("Name is mandatory")
        return self._contact

if __name__ == "__main__":
    try:
        person = (ContactAssembler()
                  .set_name("Alice Smith")
                  .set_phone("+1234567890")
                  .set_email("alice", "example.com")
                  .create())
        print(person)
    except ValueError as e:
        print("Error:", e)