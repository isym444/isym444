with open("questions.txt", "r") as f:
    all_questions = f.read().split("\n")

qa_dict = {}
for each_question in all_questions:
    qa_dict[each_question.split(',')[0]] = each_question.split(',')[1]

print(qa_dict)

print("Let's play a quiz. I will ask you a bunch of questions and you have to give me your best answers. After each question I'll tell you whether you got the answer correct and if not, I'll tell you what the right answer was. At the end of the quiz, I'll tell you how well you did!")
user_score = 0

for q, a in qa_dict.items():
    print(q)
    user_ans = input("Please enter your response: ")
    if(user_ans.lower()==a.lower()):
        print("That was the right answer!")
        user_score += 1
    else:
        print(f"Sorry, that was the wrong answer. The right answer was: {a}")

print(f"You scored {user_score} out of {len(qa_dict)}")
