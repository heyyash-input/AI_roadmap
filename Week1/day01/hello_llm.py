import os 
from pathlib import Path 
from dotenv import load_dotenv
from groq import Groq 

# load api 
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

#If not then raise an error
if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

Client = Groq(api_key=my_api_key)
Model = "openai/gpt-oss-20b"  

role = "user"
prompt = "Write a short poem about the beauty of nature."

message = {
    "role": role,
    "content": prompt
}

messages = [message]

response = Client.chat.completions.create(model=Model,messages=messages)

# print(response)

# get perfect answer
answer = response.choices[0].message.content
print("Answer:", answer)