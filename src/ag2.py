import asyncio
import os
from azure.core.exceptions import ResourceNotFoundError
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential

async def main():
    async with AzureCliCredential() as credential:
        model_name = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        if not model_name:
            raise RuntimeError(
                "Environment variable AZURE_AI_MODEL_DEPLOYMENT_NAME is required.\n"
                "Set it to your Azure AI model deployment name (for example: 'gpt-4')."
            )

        async with AzureAIClient(credential=credential, agent_name="joke-agent").create_agent(
            instructions="You are good at telling jokes.",
            model=model_name,
            name="joke-agent",
        ) as agent:
            try:
                result = await agent.run("Tell me a joke about a pirate.")
                print(result.text)
            except ResourceNotFoundError as exc:
                print("Resource not found (404) when creating or using the agent.")
                print(f"AZURE_AI_PROJECT_ENDPOINT={os.environ.get('AZURE_AI_PROJECT_ENDPOINT')}")
                print(f"AZURE_AI_MODEL_DEPLOYMENT_NAME={os.environ.get('AZURE_AI_MODEL_DEPLOYMENT_NAME')}")
                print("Verify the project endpoint and model deployment name exist in your Azure AI project.")
                raise

if __name__ == "__main__":
    asyncio.run(main())