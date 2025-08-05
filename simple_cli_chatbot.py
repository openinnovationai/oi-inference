"""
This script is a simple chatbot that uses the OpenAI API to chat with your
deployed model on OICM Deployments. It uses the OpenAI Python SDK to create
a chat completion request and stream the response.

You need to have the OpenAI Python SDK installed. Install the dependencies:

```bash
pip install openai termcolor
```

Run the script with your OICM API key and deployment ID:

```bash
export OI_API_KEY=<your-api-key>
export DEPLOYMENT_ID=<your-deployment-id>
python simple_cli_chatbot.py
```

NOTE: This was tested against a deployment of the HuggingFaceTB/SmolLM2-135M-Instruct
via the vLLM backend.
"""

import os
import sys
from typing import List

from openai import OpenAI
from openai.types.chat.chat_completion_message_param import (
    ChatCompletionMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from termcolor import colored

##
# Configuration
#

# Your OICM API key, you can also paste the key here.
OI_API_KEY = os.getenv("OI_API_KEY")
# Your OICM deployment ID, you can also paste the ID here.
DEPLOYMENT_ID = os.getenv("DEPLOYMENT_ID")
# HuggingFace model name of your deployed model.
MODEL_NAME = "HuggingFaceTB/SmolLM2-135M-Instruct"
# Base URL of the OICM API, you can find this on Deployments > [Your deployment] > Inference tab.
BASE_URL = (
    f"https://inference.member1.stg.openinnovation.ai/models/{DEPLOYMENT_ID}/proxy/v1"
)

if not OI_API_KEY or not DEPLOYMENT_ID:
    print("Error: OI_API_KEY or DEPLOYMENT_ID environment variable not set")
    print("Please set it with: export OI_API_KEY='your-key-here'")
    print("and export DEPLOYMENT_ID='your-deployment-id-here'")
    sys.exit(1)


##
# Helper functions
#


def create_message(role: str, content: str) -> ChatCompletionMessageParam:
    """Create a message using the appropriate OpenAI message type."""

    if role == "user":
        return ChatCompletionUserMessageParam(role=role, content=content)
    elif role == "assistant":
        return ChatCompletionAssistantMessageParam(role=role, content=content)
    elif role == "system":
        return ChatCompletionSystemMessageParam(role=role, content=content)
    else:
        raise ValueError(f"Invalid role: {role}")


##
# Main
#


def main():
    # Initialize OpenAI client
    client = OpenAI(base_url=BASE_URL, api_key=OI_API_KEY)

    # Initialize conversation history
    messages: List[ChatCompletionMessageParam] = [
        create_message("system", "You are a helpful AI assistant.")
    ]

    print(colored("Welcome to OpenAI Chat! (Press Ctrl+C to exit)", "green"))

    try:
        while True:
            # Get user input
            user_input = input(colored("You: ", "yellow")).strip()
            if not user_input:
                continue

            # Add user message to history
            messages.append(create_message("user", user_input))

            try:
                # Get response from OpenAI
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.7,
                    stream=True,
                )

                # Print "Assistant:" prefix first
                print(colored("Assistant:", "cyan"), end=" ")

                # Stream and print tokens as they arrive
                assistant_response = ""
                for token in response:
                    content = token.choices[0].delta.content or ""
                    if content:
                        print(colored(content, "white"), end="", flush=True)
                        assistant_response += content
                        messages.append(create_message("assistant", content))

                # Print a newline at the end
                print()

            except Exception as e:
                print(colored(f"Error: {str(e)}", "red"))
                continue

    except KeyboardInterrupt:
        print(colored("\nGoodbye!", "green"))


if __name__ == "__main__":
    main()
