import argparse
import asyncio

from fastmcp import Client

from host_apps.mcp_client_ui.menu import choose_tool, get_arguments, print_result

DEFAULT_URL = 'http://169.254.176.190:8080/mcp'


async def run_client(url):
    async with Client(url) as client:
        tools = await client.list_tools()
        if not tools:
            print('The server did not report any tools.')
            return

        while True:
            tool = await choose_tool(tools)
            if tool is None:
                return

            arguments = await get_arguments(tool)
            if arguments is None:
                continue

            print(f'Calling {tool.name}...')
            try:
                result = await client.call_tool(tool.name, arguments)
                print_result(result)
            except Exception as error:
                print(f'Tool call failed: {error}')


def main():
    parser = argparse.ArgumentParser(description='Interact with an MCP server.')
    parser.add_argument('--url', default=DEFAULT_URL, help='MCP server URL')
    args = parser.parse_args()

    try:
        asyncio.run(run_client(args.url))
    except KeyboardInterrupt:
        print('\nGoodbye.')
    except Exception as error:
        print(f'Could not connect to the MCP server: {error}')
        raise SystemExit(1) from error


if __name__ == '__main__':
    main()
