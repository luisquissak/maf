import asyncio
import os
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
gpt_api_key = os.getenv("GPT_API_KEY")

async def main():
    agent = ChatCompletionAgent(
        service=AzureChatCompletion(api_key=gpt_api_key, endpoint=openai_endpoint, deployment_name=openai_deployment_name),
        name="SK-Assistant",
        instructions="You are a helpful assistant.",
    )

    # Get a response to a user message
    response = await agent.get_response(messages="Write a haiku about Semantic Kernel.")
    print(response.content)

asyncio.run(main()) 
