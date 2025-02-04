#!/usr/bin/env python3
import argparse
import fnmatch
import pathlib
import os
import sys
from typing import List, Optional

import pathspec

# Try to import settings from config.py, if available.
try:
    import config
except ImportError:
    config = None

def guess_language(ext: str) -> str:
    """
    Determine the language for a given file extension.
    If config.LANGUAGE_MAPPING is defined, use it; otherwise, fall back to a minimal default mapping.
    """
    ext = ext.lower()
    if config and hasattr(config, "LANGUAGE_MAPPING"):
        return config.LANGUAGE_MAPPING.get(ext, '')
    # Fallback default mapping.
    default_mapping = {
        '.py': 'python',
        '.rs': 'rust',
        '.toml': 'toml',
        '.json': 'json',
        '.env': 'bash',
        '.sh': 'bash',
        '.md': 'markdown',
        '.html': 'html',
        '.css': 'css',
        '.js': 'javascript',
    }
    return default_mapping.get(ext, '')

def load_gitignore_specs(root: pathlib.Path) -> Optional[pathspec.PathSpec]:
    """
    Find all .gitignore files in the given root folder (recursively),
    adjust their patterns to be relative to the repository root,
    and compile a single PathSpec.
    """
    patterns = []
    try:
        for gitignore in root.rglob(".gitignore"):
            try:
                lines = gitignore.read_text(encoding="utf-8").splitlines()
            except Exception as e:
                print(f"Warning: Could not read {gitignore}: {e}", file=sys.stderr)
                continue
            try:
                rel_dir = gitignore.parent.relative_to(root)
            except ValueError:
                rel_dir = pathlib.Path("")
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if rel_dir != pathlib.Path(""):
                    if line.startswith("/"):
                        pattern = str(rel_dir / line.lstrip("/"))
                    else:
                        pattern = str(rel_dir / line)
                else:
                    pattern = line
                patterns.append(pattern)
        # Always ignore any .gitignore file itself.
        patterns.append("**/.gitignore")
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    except Exception as e:
        print(f"Error loading .gitignore specifications: {e}", file=sys.stderr)
        return None

def should_include_file(
    file: pathlib.Path,
    root: pathlib.Path,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    gitignore_spec: Optional[pathspec.PathSpec] = None,
) -> bool:
    """
    Decide whether a file should be included based on:
      1. Gitignore rules (if provided)
      2. CLI include/exclude glob patterns
    The patterns are matched against the file’s relative path (using POSIX-style paths).

    - If include_patterns is provided, a file is included only if it matches at least one.
    - If the file matches any exclude pattern or a gitignore rule it is omitted.
    """
    try:
        rel = file.relative_to(root)
    except ValueError:
        rel = file
    rel_str = str(rel).replace(os.sep, "/")
    if gitignore_spec and gitignore_spec.match_file(rel_str):
        return False
    if include_patterns:
        if not any(fnmatch.fnmatch(rel_str, pattern) for pattern in include_patterns):
            return False
    if exclude_patterns:
        if any(fnmatch.fnmatch(rel_str, pattern) for pattern in exclude_patterns):
            return False
    return True

def build_tree(paths: List[pathlib.Path]) -> dict:
    """
    Build a nested dictionary representing a directory tree from a list of relative file paths.
    Each key is a directory or file name; directories map to further dictionaries.
    """
    tree = {}
    for path in paths:
        parts = path.parts  # e.g., ('server', 'src', 'main.rs')
        current = tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]
    return tree

def format_tree(tree: dict, indent: str = "") -> List[str]:
    """
    Recursively format the nested dictionary tree into a list of strings.
    Directories are suffixed with a " >" symbol.
    """
    lines = []
    for key in sorted(tree.keys()):
        if tree[key]:
            lines.append(f"{indent}{key} >")
            lines.extend(format_tree(tree[key], indent + "    "))
        else:
            lines.append(f"{indent}{key}")
    return lines

def generate_markdown(
    root_path: pathlib.Path,
    output_file: str,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    gitignore_spec: Optional[pathspec.PathSpec] = None,
) -> None:
    """
    Generate a Markdown document containing:
      1. A directory tree (table of contents) showing only the files that match the filters.
      2. For each included file, a section with the file’s path and its contents inside a
         fenced code block (with syntax highlighting if possible).

    The include and exclude patterns are applied relative to the codebase root.
    """
    base = root_path.parent

    included_files = []
    try:
        for file in sorted(root_path.rglob("*")):
            if file.is_file() and should_include_file(file, root_path, include_patterns, exclude_patterns, gitignore_spec):
                try:
                    rel_file = file.relative_to(base)
                except ValueError:
                    rel_file = file
                included_files.append(rel_file)
    except Exception as e:
        print(f"Error scanning directory '{root_path}': {e}", file=sys.stderr)
        sys.exit(1)

    if not included_files:
        print("Warning: No files found matching the criteria.", file=sys.stderr)

    try:
        tree_dict = build_tree(included_files)
        tree_lines = format_tree(tree_dict)
        tree_str = "\n".join(tree_lines)
    except Exception as e:
        print(f"Error building directory tree: {e}", file=sys.stderr)
        sys.exit(1)

    md_lines = []
    md_lines.append(f"# Codebase: {root_path.name}")
    md_lines.append("")
    md_lines.append("## Directory Tree")
    md_lines.append("")
    md_lines.append("```")
    md_lines.append(tree_str)
    md_lines.append("```")
    md_lines.append("")
    md_lines.append("## Files")
    md_lines.append("")

    for rel_path in included_files:
        md_lines.append(f"### {rel_path}")
        md_lines.append("")
        file_path = base / rel_path
        ext = file_path.suffix
        language = guess_language(ext)
        md_lines.append(f"```{language}")
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            content = f"Error reading file: {e}"
        md_lines.append(content)
        md_lines.append("```")
        md_lines.append("")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"Markdown file generated: {output_file}")
    except Exception as e:
        print(f"Error writing to output file '{output_file}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Markdown document documenting a codebase. "
            "The document includes a directory tree (as a table of contents) and file contents with syntax highlighting. "
            "Optionally, you can provide include/exclude glob patterns (relative to the codebase root) to filter files. "
            "Files matching any .gitignore rules or hardcoded exclusions in config.py will be omitted. "
            "Use --no-gitignore to disable applying .gitignore rules."
        )
    )
    parser.add_argument("input", help="Path to the codebase directory")
    parser.add_argument(
        "-o",
        "--output",
        default="codebase.md",
        help="Output Markdown file (default: codebase.md)",
    )
    parser.add_argument(
        "--include",
        nargs="+",
        help=(
            "Glob pattern(s) for files to include (relative to the codebase root). "
            "Only files matching at least one pattern will be included."
        ),
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        help=(
            "Glob pattern(s) for files to exclude (relative to the codebase root). "
            "Files matching any of these patterns will be omitted."
        ),
    )
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Disable applying .gitignore file exclusions.",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.input)
    if not root.exists() or not root.is_dir():
        parser.error(f"The input path '{args.input}' is not a valid directory.")

    # Conditionally load .gitignore specifications.
    if args.no_gitignore:
        gitignore_spec = None
    else:
        gitignore_spec = load_gitignore_specs(root)

    # Merge CLI-provided exclude patterns with any hardcoded exclusions from config.py.
    cli_excludes = args.exclude if args.exclude else []
    if config and hasattr(config, "HARD_CODED_EXCLUDES"):
        combined_excludes = cli_excludes + config.HARD_CODED_EXCLUDES
    else:
        combined_excludes = cli_excludes

    try:
        generate_markdown(
            root_path=root,
            output_file=args.output,
            include_patterns=args.include,
            exclude_patterns=combined_excludes,
            gitignore_spec=gitignore_spec,
        )
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Fatal error: {err}", file=sys.stderr)
        sys.exit(1)
