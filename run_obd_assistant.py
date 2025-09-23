import json
import ollama

# Load the JSON knowledge base
with open(r"D:\DevTools\Projects\LLMS\obd_codes.json", "r") as f:
    obd_data = json.load(f)

# Function to retrieve code info
def get_code_info(code):
    for entry in obd_data:
        if entry["code"].upper() == code.upper():
            return entry
    return None


def explain_obd_code(code):
    info = get_code_info(code)
    if not info:
        return f"Sorry, I don't have information on code {code}."

    # Build a structured prompt for the model
    prompt = f"""
You are an automotive diagnostic assistant. 
The vehicle has triggered OBD-II code {code}.
Here is the structured info:
Description: {info['description']}
Possible causes: {', '.join(info['causes'])}
Severity: {info['severity']}

Explain this to the driver in plain language, with suggested actions.
"""
    response = ollama.chat(model="car-assistant", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Example usage
if __name__ == "__main__":
    while True:
        code = input("\nEnter OBD-II code (or 'exit' to quit): ").strip()
        if code.lower() == "exit":
            break
        explanation = explain_obd_code(code)
        print(f"\n{code} => {explanation}")
