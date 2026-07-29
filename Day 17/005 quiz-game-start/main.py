class Question:
    """Models a single True/False question with its text and correct answer."""

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer


class QuizBrain:
    """Handles quiz logic: tracking progress, asking questions, checking answers."""

    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list

    def still_has_questions(self):
        """Returns True if there are more questions left in the quiz."""
        return self.question_number < len(self.question_list)

    def next_question(self):
        """Displays the next question and checks the user's answer."""
        current_question = self.question_list[self.question_number]
        self.question_number += 1

        user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False): ")
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        """Compares user's answer with the correct answer and updates the score."""
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            print("You got it right!")
        else:
            print("That's wrong.")

        print(f"The correct answer was: {correct_answer}")
        print(f"Your current score is: {self.score}/{self.question_number}\n")


question_data = [
    {"text": "A slug's blood is green.", "answer": "True"},
    {"text": "The Great Wall of China is visible from space.", "answer": "False"},
    {"text": "In 1386 a French court sentenced a pig to death for murder.", "answer": "True"},
    {"text": "A shrimp's heart is in its head.", "answer": "True"},
    {"text": "Google was originally called Backrub.", "answer": "True"},
    {"text": "Python was named after the programming language.", "answer": "False"},
]


def run_quiz():
    question_bank = []
    for question in question_data:
        new_question = Question(question["text"], question["answer"])
        question_bank.append(new_question)

    quiz = QuizBrain(question_bank)

    while quiz.still_has_questions():
        quiz.next_question()

    print("You've completed the quiz!")
    print(f"Your final score was: {quiz.score}/{quiz.question_number}")


if __name__ == "__main__":