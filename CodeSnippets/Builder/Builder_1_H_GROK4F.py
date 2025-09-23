class Email:
    def __init__(self, sender, recipient, subject, body, attachments=None, priority='normal'):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.priority = priority

    def __str__(self):
        att_str = f" with {len(self.attachments)} attachments" if self.attachments else ""
        return f"Email from {self.sender} to {self.recipient}: {self.subject}{att_str} (Priority: {self.priority})"

class EmailComposer:
    def __init__(self, sender):
        if not sender or '@' not in sender:
            raise ValueError("Invalid sender email address")
        self.sender = sender
        self.recipient = None
        self.subject = None
        self.body = None
        self.attachments = []
        self.priority = 'normal'

    def to(self, recipient):
        if not recipient or '@' not in recipient:
            raise ValueError("Invalid recipient email address")
        self.recipient = recipient
        return self

    def subject(self, subject):
        if not subject:
            raise ValueError("Subject cannot be empty")
        self.subject = subject
        return self

    def body(self, body):
        if not body:
            raise ValueError("Body cannot be empty")
        self.body = body
        return self

    def attach(self, file_path):
        if len(self.attachments) >= 5:
            raise ValueError("Maximum 5 attachments allowed")
        if not file_path:
            raise ValueError("Invalid file path for attachment")
        self.attachments.append(file_path)
        return self

    def set_priority(self, priority):
        valid_priorities = ['low', 'normal', 'high']
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")
        self.priority = priority
        return self

    def reset(self):
        self.recipient = None
        self.subject = None
        self.body = None
        self.attachments = []
        self.priority = 'normal'
        return self

    def build(self):
        if not self.recipient:
            raise ValueError("Recipient is required")
        if not self.subject:
            raise ValueError("Subject is required")
        if not self.body:
            raise ValueError("Body is required")
        return Email(self.sender, self.recipient, self.subject, self.body, self.attachments, self.priority)

class EmailDirector:
    def __init__(self, composer):
        self.composer = composer

    def create_welcome_email(self, recipient):
        self.composer.to(recipient).subject("Welcome!").body("Thank you for joining us.").set_priority('normal')
        return self.composer.build()

    def create_urgent_notification(self, recipient, details):
        self.composer.to(recipient).subject("Urgent: Action Required").body(details).set_priority('high').attach("urgent_doc.pdf")
        return self.composer.build()

if __name__ == "__main__":
    try:
        composer = EmailComposer("sender@example.com")
        email1 = composer.to("user@example.com").subject("Hello").body("This is a test.").build()
        print(email1)

        director = EmailDirector(composer.reset())
        email2 = director.create_welcome_email("newuser@example.com")
        print(email2)

        composer = EmailComposer("sender@example.com")
        email3 = director.create_urgent_notification("admin@example.com", "System alert: Check logs immediately.")
        print(email3)

        # Edge case: invalid recipient
        composer = EmailComposer("sender@example.com")
        try:
            composer.to("invalid-email").build()
        except ValueError as e:
            print(f"Error: {e}")

        # Edge case: too many attachments
        composer = EmailComposer("sender@example.com").to("user@example.com").subject("Test").body("Test")
        for i in range(6):
            composer.attach(f"file_{i}.pdf")
    except ValueError as e:
        print(f"Error: {e}")