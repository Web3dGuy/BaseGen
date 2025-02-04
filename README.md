
---

# BaseGen

**BaseGen** is a Python CLI tool that generates a comprehensive Markdown document from a codebase. The generated Markdown file includes:

- **A Directory Tree:** A table-of-contents view of your codebase.
- **File Sections:** Each file (or a filtered subset) is rendered with its contents inside a fenced code block using syntax highlighting.

This tool is especially useful for creating AI-ready backups of your source code or for code analysis. It supports flexible file filtering and can automatically honor your repository’s `.gitignore` files (or ignore them when desired) as well as custom exclusion settings defined in a separate configuration file.

---

## Features

- **Directory Tree Generation:**  
  Recursively scans your codebase and produces a hierarchical view of folders and files, which is then rendered as a code block in the output Markdown file.

- **Syntax Highlighting:**  
  Uses a comprehensive file-extension-to-language mapping (configured in `config.json`) so that code blocks are tagged appropriately for syntax highlighting in editors such as VS Code. (If no configuration is provided, a default minimal mapping is used.)

- **Flexible File Filtering:**  
  - Use the `--include` flag to restrict processing to files matching one or more glob patterns (relative to the codebase root).  
  - Use the `--exclude` flag to omit files matching specified glob patterns. These CLI-specified exclusions are merged with a set of hardcoded exclusions defined in `config.json` (which typically omit images, text files, package lock files, etc.).

- **.gitignore Support (and Optional Disabling):**  
  By default, BaseGen scans your codebase for any `.gitignore` files and excludes matching files from the output. You can disable this behavior by using the `--no-gitignore` flag.

- **Configurable via `config.json`:**  
  Additional settings—such as hardcoded file and folder exclusions (`HARD_CODED_EXCLUDES`) and the mapping from file extensions to language identifiers (`LANGUAGE_MAPPING`)—are stored in `config.json`. This allows you to easily customize the behavior without modifying the main script.

---

## Installation

1. **Clone the Repository** (if applicable):

   ```
   git clone https://github.com/Web3dGuy/BaseGen.git
   cd basegen
   ```

2. **Install Dependencies:**

   BaseGen requires Python 3.6+ and the third-party [`pathspec`](https://pypi.org/project/pathspec/) package. Install it via pip:

   ```
   pip install pathspec
   ```

---

## Configuration

BaseGen reads additional settings from a `config.json` file located in the same directory as the main script. An example configuration is provided (typically named `example.config.json`); you should rename or copy it to `config.json` and adjust as needed.

The configuration file defines:

- **HARD_CODED_EXCLUDES:**  
  A list of glob patterns that automatically exclude files that are generally not needed for debugging or code analysis (for example, documentation files like `.md` and `.txt`, images, audio files, and package lock files).

- **LANGUAGE_MAPPING:**  
  A comprehensive dictionary mapping file extensions to language identifiers (based on the languages supported by highlight.js). This mapping ensures that the fenced code blocks in the generated Markdown file are tagged appropriately for syntax highlighting.

---

## Usage

BaseGen is invoked from the command line. The main script is named **basegen.py**.

### Basic Example

Generate a Markdown file for the entire codebase:

```
python basegen.py /path/to/your/codebase
```

This command creates a file named `codebase.md` in the current directory.

### Custom Output Filename

Specify a different output filename with the `-o` flag:

```
python basegen.py /path/to/your/codebase -o mycode.md
```

### Filtering Files

- **Include Files:**  
  Only include files that match the specified glob patterns (relative to the codebase root):

  ```
  python basegen.py /path/to/your/codebase --include "*.rs" "*.toml"
  ```

- **Exclude Files:**  
  Exclude files that match the specified glob patterns:

  ```
  python basegen.py /path/to/your/codebase --exclude "src/db/*"
  ```

*Note:* The exclusions you specify via `--exclude` are merged with the hardcoded exclusions defined in `config.json`.

### Disabling .gitignore Exclusions

By default, BaseGen respects `.gitignore` files found in your codebase. To disable this behavior and include files regardless of any `.gitignore` entries, use the `--no-gitignore` flag:

```
python basegen.py /path/to/your/codebase --no-gitignore
```

---

## How It Works

1. **Scanning:**  
   BaseGen recursively scans the specified codebase directory to identify all files.

2. **Filtering:**  
   Files are filtered out based on three criteria:
   - Files that match patterns in any `.gitignore` files (unless `--no-gitignore` is used).
   - Hardcoded exclusion patterns defined in `config.json`.
   - Additional include and exclude glob patterns provided via the command line.

3. **Markdown Generation:**  
   The tool generates a Markdown document that includes:
   - A **Directory Tree** (rendered as a code block) that shows the structure of the codebase.
   - **File Sections:** For each included file, a header is generated with the file’s relative path, followed by the file’s content enclosed in a fenced code block. The block is tagged with the appropriate language identifier (determined via `config.json` or a default mapping) so that syntax highlighting is applied in supported editors.

---

## Command-Line Flags Summary

- **`input` (positional):**  
  The path to the codebase directory to be processed.

- **`-o, --output`:**  
  Specifies the output Markdown file name. (Default: `codebase.md`)

- **`--include`:**  
  One or more glob patterns specifying which files to include (relative to the codebase root). Only files matching at least one of these patterns will be processed.

- **`--exclude`:**  
  One or more glob patterns specifying files to exclude (relative to the codebase root). Files matching any of these patterns will be omitted. These are merged with the hardcoded exclusions in `config.json`.

- **`--no-gitignore`:**  
  Disables the processing of `.gitignore` files. When set, files are not filtered out based on `.gitignore` rules.

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request on GitHub.

---

## License

MIT License

Copyright (c) 2024 Web3dGuy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

Happy coding and enjoy using BaseGen!

---
