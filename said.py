import os
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the Hugging Face API key from an environment variable
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Define the model and tokenizer
model_name = "WormGPT"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=HUGGINGFACE_API_KEY)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=HUGGINGFACE_API_KEY)

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=200, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def chatbot():
    print("Welcome to the Uncensored AI Chatbot powered by WormGPT!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        response = generate_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot()