import streamlit as st
import json
import random
import os
from datetime import datetime

class Quiz:
    def __init__(self, filename):
        self.questions = self.load_questions(filename)
        self.results = []

    def load_questions(self, filename):
        questions = []
        with open(filename, 'r') as file:
            question_data = {}
            for line in file:
                line = line.strip()
                if line.startswith("Question:"):
                    question_data["question"] = line[9:].strip()
                    question_data["options"] = []
                elif line.startswith(("A:", "B:", "C:", "D:")):
                    question_data["options"].append(line[2:].strip())
                elif line.startswith("Correct:"):
                    correct_answer_str = line[8:].strip()
                    question_data["correct_answer"] = ord(correct_answer_str) - ord('A')
                    questions.append(question_data)
                    question_data = {}
        return questions

    def take_quiz(self, num_questions):
        if num_questions > len(self.questions):
            print(f"You have requested {num_questions} questions, but there are only {len(self.questions)} available.")
            num_questions = len(self.questions)
            print(f"Quiz will proceed with {num_questions} questions.")
        
        shuffled_questions = random.sample(self.questions, num_questions)

        score = 0
        for i, q in enumerate(shuffled_questions):
            print(f"\nQuestion {i+1}: {q['question']}")
            for j, option in enumerate(q['options']):
                print(f"{chr(65+j)}. {option}")
            
            answer = input("Enter your answer (A-D): ").upper()
            answer_index = ord(answer) - ord('A')
            is_correct = answer_index == q['correct_answer']
            if is_correct:
                score += 1
            
            self.results.append({
                "question_index": i,
                "question": q['question'],
                "options": q['options'],
                "correct_answer": q['correct_answer'],
                "user_answer": answer_index,
                "is_correct": is_correct
            })
        
        print("\n--- Quiz Results ---")
        for i, result in enumerate(self.results):
            print(f"\nQuestion {i+1}: {result['question']}")
            print("Options:")
            for j, option in enumerate(result['options']):
                print(f"  {chr(65+j)}. {option}")
            correct_answer_letter = chr(65 + result['correct_answer'])
            print(f"Correct Answer: {correct_answer_letter}")
            
            user_answer_letter = chr(65 + result['user_answer']) if 0 <= result['user_answer'] < len(result['options']) else "N/A"
            print(f"Your Answer: {user_answer_letter}")
            
            if result['is_correct']:
                print("Result: Correct!")
            else:
                print("Result: Incorrect.")
        
        print(f"\n--- Final Score: {score} out of {num_questions} ---")
        self.save_results()

    def save_results(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quiz_results_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump({
                "questions": self.questions,
                "results": self.results
            }, f, indent=2)
        print(f"Results saved to {filename}")

def get_available_topics():
    topics = []
    for file in os.listdir():
        if file.endswith(".txt") and file != "questions.txt":
            topics.append(file[:-4].replace("_", " ").title())
    return topics

def main():
    topics = get_available_topics()
    
    while True:
        print("\n1. Take a quiz")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            print("\nAvailable topics:")
            for i, topic in enumerate(topics, 1):
                print(f"{i}. {topic}")
            
            topic_choice = int(input("Choose a topic number: ")) - 1
            if 0 <= topic_choice < len(topics):
                filename = f"{topics[topic_choice].lower().replace(' ', '_')}.txt"
                quiz = Quiz(filename)
                
                num_questions = int(input("How many questions would you like to take? "))
                quiz.take_quiz(num_questions)
            else:
                print("Invalid topic choice.")
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
