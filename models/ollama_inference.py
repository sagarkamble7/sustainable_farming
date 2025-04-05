import ollama

def generate_response(prompt):
    response = ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']
