import json 
from fuzzywuzzy import process
import spacy 
from dotenv import load_dotenv
import os 

# Loading spaCy model
nlp = spacy.load('en_core_web_sm')

# Loading environment variables
load_dotenv()


# Loading knowledge from JSON file
def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"questions": []}
    except json.JSONDecodeError:
        return {"questions": []}


# Saving knowledge base to a JSON file 
def save_knowledge_base(file_path: str, data: dict):    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


# Finding best match from the users question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    best_match, score = process.extractOne(user_question, questions)
    return best_match if score >= 70 else None




# Getting answer for a matched question
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question: 
            return q["answer"]
    return None


# Idk what this is but it was part of the new NLP?
def preprocess_text(text: str) -> str: 
    doc = nlp(text)
    return ' '.join(token.lemma_ for token in doc if not token.is_stop)




# Main function
def chatbot():
    knowledge_base_file = os.getenv('KNOWLEDGE_BASE_FILE', 'knowledge_base.json')
    knowledge_base = load_knowledge_base(knowledge_base_file)
    questions = [q["question"] for q in knowledge_base["questions"]]  # Load questions once

    while True:
        user_input = input('You: ')

        if user_input.lower() == 'quit':
            break

        # Preprocess user input
        preprocessed_input = preprocess_text(user_input)

        best_match = find_best_match(preprocessed_input, questions)

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                questions.append(user_input)  # Update the questions list
                save_knowledge_base(knowledge_base_file, knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chatbot()

