class ValidatorHelper:
    def __init__(self, data: dict):
        self.data = data
        self.errors = {}

    def required(self, field, message=None):
        value = self.data.get(field)
        if not value or (isinstance(value, str) and not value.strip()):
            self.errors[field] = message or f"{field} is required"

    def validate(self):
        if self.errors:
            raise ValueError(str(self.errors))