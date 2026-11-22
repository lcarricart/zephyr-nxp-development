import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    # Open an MCP Streamable HTTP connection to the board.
    async with streamable_http_client('http://169.254.176.190:8080/mcp') as streams:
        async with ClientSession(*streams, read_timeout_seconds=35) as session:
            # Negotiate the protocol and establish the MCP session.
            info = await session.initialize()
            print('Connected:', info.server_info.name, 'protocol:', info.protocol_version, flush=True)

            # Sends the MCP tools/list request and prints the tool names.
            tools = await session.list_tools()
            print('Tools:', ', '.join(tool.name for tool in tools.tools), flush=True)

            # These dictionaries are only tool arguments; the MCP library wraps them
            # in full JSON-RPC tools/call messages with method, ID, and parameters.
            for name, args in [('led_control', {'action': 'off'}),
                               ('led_control', {'action': 'on'}),
                               ('delayed_response', {'message': 'test'})]:
                result = await session.call_tool(name=name, arguments=args)
                print(name, args, result.model_dump_json(exclude_none=True), flush=True)

asyncio.run(main())
