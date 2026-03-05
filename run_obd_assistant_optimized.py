import json
import ollama
import os
import time

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

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

    # structured prompt for the model
    prompt = f"""
You are an automotive diagnostic assistant. 
The vehicle has triggered OBD-II code {code}.
Here is the structured info:
Description: {info['description']}
Possible causes: {', '.join(info['causes'])}
Severity: {info['severity']}

Explain this to the driver in plain language, with suggested changes to their driving if needed.
"""
    response = ollama.chat(model="car-assistant",
                           messages=[{"role": "user", "content": prompt}],
                           stream=True,
                           options={"num_gpu":99, "num_ctx": 512},
                           keep_alive="10m")

    for info in response:
        print(info['message']['content'], end='', flush=True)

# Example usage
if __name__ == "__main__":
    while True:
        code = input("\nEnter OBD-II code (or 'exit' to quit): ").strip()
        if code.lower() == "exit":
            break
        explain_obd_code(code)
