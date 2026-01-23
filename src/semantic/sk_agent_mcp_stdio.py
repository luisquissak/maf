
import asyncio
import os
import sys
from pathlib import Path

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments

from semantic_kernel.connectors.mcp import MCPStdioPlugin


openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
gpt_api_key = os.getenv("GPT_API_KEY")  # no padrão Azure costuma ser AZURE_OPENAI_API_KEY


async def main():
    # 1) Kernel + serviço Azure OpenAI
    kernel = Kernel()

    chat_service = AzureChatCompletion(
        api_key=gpt_api_key,
        endpoint=openai_endpoint,
        deployment_name=openai_deployment_name,
        service_id="azure",
        # Dica: se você tiver problemas de parâmetro "parallel_tool_calls",
        # defina um api_version mais recente aqui.
        # api_version="2024-10-21"
    )
    kernel.add_service(chat_service)

    # 2) Habilita function calling (auto) para o modelo poder escolher ferramentas
    settings = AzureChatPromptExecutionSettings(
        service_id="azure",
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    # 3) Sobe/conecta no MCP server local via STDIO (subprocess)
    server_path = str(Path(__file__).with_name("mcp_server_calc.py"))

    async with MCPStdioPlugin(
        name="Calc",
        description="Ferramentas de calculadora via MCP (stdio)",
        command=sys.executable,            # usa o python do seu .venv
        args=[server_path],
    ) as calc_plugin:

        # 4) Agente com plugin MCP
        agent = ChatCompletionAgent(
            kernel=kernel,
            name="SK-Assistant",
            instructions=(
                "Você é um assistente útil. "
                "Quando precisar fazer contas, use as ferramentas do plugin Calc."
            ),
            plugins=[calc_plugin],
            arguments=KernelArguments(settings=settings),
        )

        # 5) Pergunta que incentiva o uso da tool
        prompt = "Quanto é 13*7 + 5? Use as ferramentas de calculadora."
        response = await agent.get_response(messages=prompt)
        print(response.content)


if __name__ == "__main__":
    asyncio.run(main())
