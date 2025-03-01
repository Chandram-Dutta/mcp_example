import os
from pathlib import Path
import shutil
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables and set up the MCP server
load_dotenv()
mcp = FastMCP("MCP Example Server")

# Set up directory configuration
ROOT_DIR = Path(os.path.expanduser(os.getenv("MCP_ROOT_DIR", "~")))
ALLOWED_SUBDIRS = set(filter(None, os.getenv("MCP_ALLOWED_SUBDIRS", "").split(",")))


def is_allowed_path(path: Path) -> bool:
    """Check if a path is within allowed subdirectories."""
    if not path.is_relative_to(ROOT_DIR):
        return False
    return any(path.is_relative_to(ROOT_DIR / subdir) for subdir in ALLOWED_SUBDIRS)


@mcp.tool()
def list_files(directory: str) -> list[str]:
    """List files in a directory within allowed subdirectories."""
    if directory.startswith("/"):
        raise ValueError("Path cannot be absolute")

    full_path = ROOT_DIR / directory

    if not full_path.is_dir():
        raise FileNotFoundError(f"Path {directory} is not a directory")
    if not is_allowed_path(full_path):
        raise ValueError(f"Path {directory} is not allowed")

    return [f.name for f in full_path.iterdir() if f.is_file()]


@mcp.tool()
def read_file(file_path: str) -> str:
    """Read the content of a file within allowed subdirectories."""
    if file_path.startswith("/"):
        raise ValueError("Path cannot be absolute")

    full_path = ROOT_DIR / file_path

    if not full_path.is_file():
        raise FileNotFoundError(f"File {file_path} does not exist")
    if not is_allowed_path(full_path):
        raise ValueError(f"Path {file_path} is not allowed")

    with open(full_path, "r") as f:
        return f.read()


@mcp.tool()
def write_file(file_path: str, content: str) -> None:
    """Write content to a file within allowed subdirectories."""
    if file_path.startswith("/"):
        raise ValueError("Path cannot be absolute")

    full_path = ROOT_DIR / file_path
    if not is_allowed_path(full_path):
        raise ValueError(f"Path {file_path} is not allowed")

    # Create parent directory if needed
    dir_path = full_path.parent
    if not dir_path.exists():
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            raise FileNotFoundError(f"Directory {dir_path} could not be created: {e}")

    try:
        with open(full_path, "w") as f:
            f.write(content)
    except (PermissionError, OSError) as e:
        raise ValueError(f"Could not write to file {file_path}: {e}")


@mcp.tool()
def create_directory(directory: str) -> None:
    """Create a new directory within allowed subdirectories."""
    if directory.startswith("/"):
        raise ValueError("Path cannot be absolute")

    full_path = ROOT_DIR / directory

    if full_path.exists():
        raise FileExistsError(f"Directory {directory} already exists")
    if not is_allowed_path(full_path):
        raise ValueError(f"Path {directory} is not allowed")

    full_path.mkdir(parents=True, exist_ok=False)


@mcp.tool()
def delete_path(path_str: str) -> None:
    """Delete a file or directory within allowed subdirectories."""
    if path_str.startswith("/"):
        raise ValueError("Path cannot be absolute")

    full_path = ROOT_DIR / path_str

    if not is_allowed_path(full_path):
        raise ValueError(f"Path {path_str} is not allowed")
    if full_path == ROOT_DIR or full_path in [
        ROOT_DIR / subdir for subdir in ALLOWED_SUBDIRS
    ]:
        raise ValueError("Cannot delete root directory or allowed subdirectories")

    if full_path.is_dir():
        shutil.rmtree(str(full_path))
    elif full_path.is_file():
        full_path.unlink()
    else:
        raise ValueError(f"Path {path_str} does not exist")


@mcp.tool()
def move_file(source_path: str, destination_path: str) -> None:
    """Move or rename a file or directory within allowed subdirectories."""
    if source_path.startswith("/") or destination_path.startswith("/"):
        raise ValueError("Paths cannot be absolute")

    full_source = ROOT_DIR / source_path
    full_destination = ROOT_DIR / destination_path

    if not is_allowed_path(full_source) or not is_allowed_path(full_destination):
        raise ValueError("Both source and destination paths must be allowed")
    if not full_source.exists():
        raise FileNotFoundError(f"Source path {source_path} does not exist")

    shutil.move(str(full_source), str(full_destination))
