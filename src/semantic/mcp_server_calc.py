
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calc-server")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Soma dois números."""
    return a + b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplica dois números."""
    return a * b

@mcp.tool()
def expression(expr: str) -> float:
    """Avalia uma expressão matemática simples (ex: '13*7+5')."""
    # ⚠️ Demonstração. Em produção, NÃO use eval puro.
    return float(eval(expr, {"__builtins__": {}}, {}))

if __name__ == "__main__":
    # STDIO: ideal para rodar local e o agente iniciar como subprocess.
    mcp.run(transport="stdio")
