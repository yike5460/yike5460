import json
import os
import re
import boto3

from dotenv import load_dotenv

load_dotenv()

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime", region_name=os.getenv("REGION_NAME")
)

default_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
default_system = "You are a helpful and knowledgeable assistant who is able to provide detailed and accurate information on a wide range of topics. You are also able to provide clear and concise answers to questions and are always willing to go the extra mile to help others."

TASK = "Draft an email responding to a customer complaint" # Replace with your task!
# Optional: specify the input variables you want Claude to use. If you want Claude to choose, you can set `variables` to an empty list!
# VARIABLES = []
VARIABLES = ["CUSTOMER_COMPLAINT", "COMPANY_NAME"]
# If you want Claude to choose the variables, just leave VARIABLES as an empty list.

# TASK = "Choose an item from a menu for me given my preferences"
# VARIABLES = []
# VARIABLES = ["MENU", "PREFERENCES"]

def generate_bedrock_response(prompt, assistant_partial, model_id):
    """
    This function generates a test dataset by invoking a model with a given prompt.

    Parameters:
    prompt (str): The user input prompt.

    Returns:
    matches (list): A list of questions generated by the model, each wrapped in <case></case> XML tags.
    """
    messages = [
        {
            "role": "user",
            "content": [
                    # {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": content_image}},
                    {"type": "text", "text": prompt}
                ],
        },
        {
            "role": "assistant",
            "content": [
                # {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": content_image}},
                {"type": "text", "text": assistant_partial},
            ],
        },
    ]
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": messages,
            "system": default_system,
        }
    )
    response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get("body").read())
    return response_body["content"][0]["text"]

def pretty_print(message):
    print('\n\n'.join('\n'.join(line.strip() for line in re.findall(r'.{1,100}(?:\s+|$)', paragraph.strip('\n'))) for paragraph in re.split(r'\n\n+', message)))

# main entry point
if __name__ == "__main__":
    
    variable_string = ""
    for variable in VARIABLES:
        variable_string += "\n{$" + variable.upper() + "}"
    print("variable_string: ", variable_string)

    # Read the PE template from the md file in lcal directory of the same name with md extension
    with open("zero2onePE.md", "r") as file:
        metaprompt = file.read()
    prompt = metaprompt.replace("{{TASK}}", TASK)
    assistant_partial = "<Inputs>"
    if variable_string:
        assistant_partial += variable_string + "\n</Inputs>\n<Instructions Structure>"
    print("assistant_partial: ", assistant_partial)
    response = generate_bedrock_response(prompt, assistant_partial, default_model_id)
    pretty_print("final response: " + response)