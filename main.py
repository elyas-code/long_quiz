from bs4 import BeautifulSoup
import time

BLUE = "\033[0;34m"
BOLD = "\033[1m"
LIGHT_GREEN = "\033[1;32m"
LIGHT_BLUE = "\033[1;34m"
YELLOW = "\033[33m"
END = "\033[0m"

class QuizQuestion:
    def __init__(self, text, choices, right, is_raw):
        if is_raw:
            self.text = text
            self.choices = [item[3:].strip() for item in choices.split('\n') if item[3:].strip()]
            self.right = right.replace('The correct answer is:', '').strip()
        else:    
            self.text = text
            self.choices = choices
            self.right = right

def main():
    start_time = time.time()
    html_doc = open('01.html').read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    questions = soup.find_all(class_='qtext')
    answers = soup.find_all(class_='answer')
    right_answers = soup.find_all(class_='rightanswer')
    quiz = []

    for i in range(len(questions)):
        question = questions[i].get_text()
        choices = answers[i].get_text()
        right_answer = right_answers[i].get_text()

        for i in quiz:
            if question == i.text:
                continue

        quiz_q = QuizQuestion(question, choices, right_answer, True)
        quiz.append(quiz_q)


    while len(quiz) > 0:
        print(YELLOW + f"{len(quiz)} questions to go, Keep going!" + END)
        for question in quiz:
            choices = []
            for i in range(len(question.choices)):
                choices.append(chr(65+i) + " " + question.choices[i])

            choices = "\n".join(choices)
            print(f'\n{BLUE + BOLD + question.text + END}\n{LIGHT_GREEN + choices}')

            user_choice = input(BOLD + LIGHT_BLUE + 'Choose: ' + END)

            try:
                if question.choices[ord(user_choice[0].upper()) - 65] == question.right:
                    quiz.remove(question)
            except:
                pass
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(BOLD + BLUE + f"\nQuiz completed in {elapsed_time:.2f} seconds." + END)

if __name__ == "__main__":
    main()
