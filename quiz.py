import json
import random
import time
from playsound import playsound

with open("questions.json", "r") as f:
    questions = json.load(f)

print("📱 Welcome to the Quiz Game!")
username = input("Enter your name: ")

categories = list(questions.keys())
print("\n📚 Available Categories:")
for idx, cat in enumerate(categories, 1):
    print(f"{idx}. {cat}")

while True:
    try:
        category_choice = int(input("Choose a category (number): "))
        if 1 <= category_choice <= len(categories):
            break
        else:
            print("❌ Invalid number. Try again.")
    except ValueError:
        print("❌ Please enter a number.")

category = categories[category_choice - 1]
selected_questions = questions.get(category, [])

if not selected_questions:
    print("❌ No questions found for this category.")
    exit()

print(f"\n🎮 Starting quiz in category: {category}\n")

score = 0

for i, q in enumerate(random.sample(selected_questions, min(5, len(selected_questions))), 1):
    print(f"\n🔹 Question {i}: {q['question']}")
    for j, opt in enumerate(q['options'], 1):
        print(f"  {j}. {opt}")

    try:
        user_ans = int(input("Your answer (1-4): "))
        if user_ans == q['answer']:
            print("✅ Correct!")
            playsound(r"D:\Python_Project\Sound\correct.wav")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer is: {q['options'][q['answer'] - 1]}")
            playsound(r"D:\Python_Project\Sound\wrong.wav")
    except ValueError:
        print("❌ Invalid input. Skipped.")
        playsound(r"D:\Python_Project\Sound\wrong.wav")

# Final Score
print(f"\n🎉 {username}, your final score is {score}/5!")
import json
import os

leaderboard_file = f"leaderboard_{category}.json"

entry = {"username": username, "score": score, "category": category}

if os.path.exists(leaderboard_file):
    with open(leaderboard_file, "r") as f:
        data = json.load(f)
else:
    data = []

data.append(entry)


print("\n🏆 Leaderboard:")
for idx, entry in enumerate(data, 1):
    print(f"{idx}. {entry['username']} - {entry['score']} points ({entry['category']})")
    
    with open(leaderboard_file, "w") as f:
        json.dump(data, f, indent=4)

print(f"🏆 Your score has been saved in {leaderboard_file}.")

# ==== LIVE LEADERBOARD ====
print("\n📊 Live Leaderboard:")

sorted_data = sorted(data, key=lambda x: x["score"], reverse=True)
for idx, entry in enumerate(sorted_data, 1): 
    
    
    print(f"{idx}. {entry['username']} - {entry['score']} points ({entry['category']})")

