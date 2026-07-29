class Question:
    """Models a single True/False question with its text and correct answer."""

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer