import openai

# Set your OpenAI API key (preferably stored securely, e.g., as an environment variable)
openai.aps_key = "chatbot_key"

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150,
        stop=None
    )
    
    return response.choices[0].text.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        
        response = chat_with_gpt(user_input)
        print("Chatbot:", response)

