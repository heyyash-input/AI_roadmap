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

# 3 prompts :
prompt1 = "Hi!"  
prompt2 = " Explain time travel concept"
prompt3 = "write the 1000 words essay on the impact of climate change on global ecosystems."

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message = {
        "role": role,
        "content": prompt
    }

    messages = [message]

    response = Client.chat.completions.create(model=Model,messages=messages , max_tokens= 50)
    usage = response.usage
    print(f"Prompt: {prompt} --> your tokens: {usage.prompt_tokens} completion_tokens: { usage.completion_tokens} total tokens: {usage.total_tokens} Finish Reason: {response.choices[0].finish_reason} ") 
    # print(response)

    # get perfect answer
    answer = response.choices[0].message.content
    print("Answer:", answer)



#prompt = "Write a short poem about the beauty of nature."

#message = {
 #   "role": role,
  #  "content": prompt
#}

#messages = [message]

#response = Client.chat.completions.create(model=Model,messages=messages)

# print(response)

# get perfect answer
#answer = response.choices[0].message.content
#print("Answer:", answer)