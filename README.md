# MCP Example Server

This is a simple demonstration of a [Model Configured Program (MCP)](https://github.com/microsoft/mcp) server. This example shows how to create a file system utility that allows LLM agents to access specific directories on your computer in a controlled way.

## What is MCP?

MCP (Model Configured Programs) is a framework developed by Anthropic to enable AI agents to interact with various tools and APIs in a controlled way.

## Features of this Example

This example implements a simple file management system that:

- Restricts access to specific subdirectories of the user's home directory (configured via environment variables)
- Provides tools for basic file operations:
  - Listing files in directories
  - Reading file contents
  - Writing to files
  - Creating directories
  - Deleting files and directories
  - Moving/renaming files

## Configuration

The server is configured using environment variables in the `.env` file:

- `MCP_ROOT_DIR`: Base directory for all operations (defaults to home directory)
- `MCP_ALLOWED_SUBDIRS`: Comma-separated list of subdirectories under root that the server can access

## Running the Server

1. Install the required dependencies:
   ```bash
   uv pip install -e .
   ```

2. Run the server:
   ```bash
   mcp install src.server -f .env
   ```

3. Connect to the server using an MCP client.

## Security Considerations

- This server restricts file operations to specific directories to prevent unauthorized access
- All paths are validated to ensure they don't escape the allowed directories
- Absolute paths are rejected to prevent path traversal attacks

This example is intended for educational purposes. In production systems, additional security measures would be recommended.