from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="hello-mcp", stateless_http=True)

@mcp.tool(name="GreetingAgent", description="Search the web for information")
def search_online(query: str) -> str:
    return f"Results for {query}..."

mcp_app = mcp.streamable_http_app()