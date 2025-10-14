class Contact:
    def __init__(self, name: str, phone_number: str):
        self.name = name
        self.phone_number = phone_number

    def __repr__(self):
        return f"<Contact name={self.name} phone={self.phone_number}"
