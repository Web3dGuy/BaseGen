# config.py

# Hardcoded file and folder exclusion patterns.
# These patterns exclude documentation, text files, image and audio assets,
# package lock files, and other files that are generally not needed for debugging or code analysis.
HARD_CODED_EXCLUDES = [
    "*.md",              # Markdown documentation files
    "*.txt","*.doc",
    "*.ttf",".otf",
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.tiff", "*.svg",  # Image files
    "*.mp3", "*.wav", "*.ogg", "*.flac",  # Audio files
    "package-lock.json",  # Package lock files (e.g., from npm)
]

# Mapping from file extensions to language identifiers for syntax highlighting.
# This mapping is based on the languages supported by highlight.js.
# (Some file extensions are ambiguous—e.g. ".m" is used by both Matlab and Objective-C;
# you may wish to adjust these mappings for your projects.)
LANGUAGE_MAPPING = {
    # 1c
    '.1c': '1c',
    # ABNF
    '.abnf': 'abnf',
    # Access log
    '.accesslog': 'accesslog',
    # ActionScript
    '.as': 'actionscript',
    # Ada (using both body and spec extensions)
    '.ada': 'ada',
    '.adb': 'ada',
    '.ads': 'ada',
    # Apache (configuration)
    '.apache': 'apache',
    '.conf': 'apache',       # common for Apache config files
    '.htaccess': 'apache',
    # AppleScript
    '.applescript': 'applescript',
    # Arduino
    '.ino': 'arduino',
    # ARM assembly – (no universal extension; using .arm as a placeholder)
    '.arm': 'armasm',
    # AsciiDoc
    '.adoc': 'asciidoc',
    '.asciidoc': 'asciidoc',
    # AspectJ
    '.aj': 'aspectj',
    # AutoHotkey
    '.ahk': 'autohotkey',
    # AutoIt
    '.au3': 'autoit',
    # Bash / Shell
    '.bash': 'bash',
    '.sh': 'bash',
    # BASIC
    '.bas': 'basic',
    # BNF (Backus–Naur Form)
    '.bnf': 'bnf',
    # Brainfuck
    '.bf': 'brainfuck',
    # C
    '.c': 'c',
    '.h': 'c',  # header files
    # C++
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.cxx': 'cpp',
    '.hpp': 'cpp',
    # C#
    '.cs': 'csharp',
    '.csharp': 'csharp',
    # CSP
    '.csp': 'csp',
    # CSS
    '.css': 'css',
    # D
    '.d': 'd',
    # Dart
    '.dart': 'dart',
    # Delphi
    '.dpr': 'delphi',
    '.dfm': 'delphi',
    # Diff / Patch
    '.diff': 'diff',
    '.patch': 'diff',
    # Django (templating)
    '.django': 'django',
    # DNS (zone files)
    '.dns': 'dns',
    # Dockerfile (typically no extension, so match the filename in your tool)
    '.dockerfile': 'dockerfile',
    # DOS / Batch
    '.bat': 'dos',
    '.cmd': 'dos',
    # DSConfig
    '.dsconfig': 'dsconfig',
    # Device Tree Source
    '.dts': 'dts',
    # Dust
    '.dust': 'dust',
    # EBNF
    '.ebnf': 'ebnf',
    # Elixir
    '.ex': 'elixir',
    '.exs': 'elixir',
    # Elm
    '.elm': 'elm',
    # ERB
    '.erb': 'erb',
    # Erlang
    '.erl': 'erlang',
    '.hrl': 'erlang',
    # Excel (if needed; not common for code)
    # FIX (Financial Information eXchange)
    '.fix': 'fix',
    # Flix
    '.flix': 'flix',
    # Fortran (fixed and free formats)
    '.f': 'fortran',
    '.for': 'fortran',
    '.f90': 'fortran',
    '.f95': 'fortran',
    '.f03': 'fortran',
    '.f77': 'fortran',
    # F#
    '.fs': 'fsharp',
    '.fsi': 'fsharp',
    '.fsx': 'fsharp',
    # GAMS
    '.gms': 'gams',
    # Gauss
    '.gauss': 'gauss',
    # G-code
    '.gcode': 'gcode',
    # Gherkin
    '.feature': 'gherkin',
    # GLSL (OpenGL Shading Language)
    '.glsl': 'glsl',
    '.frag': 'glsl',
    '.vert': 'glsl',
    # Go
    '.go': 'go',
    # Golo
    '.golo': 'golo',
    # Gradle
    '.gradle': 'gradle',
    # Groovy
    '.groovy': 'groovy',
    # Haml
    '.haml': 'haml',
    # Handlebars
    '.handlebars': 'handlebars',
    '.hbs': 'handlebars',
    # Haskell
    '.hs': 'haskell',
    # Haxe
    '.hx': 'haxe',
    # HSP
    '.hsp': 'hsp',
    # HTML
    '.html': 'html',
    '.htm': 'htm',
    # HTMLBars
    '.htmlbars': 'htmlbars',
    # HTTP
    '.http': 'http',
    # Hy
    '.hy': 'hy',
    # Inform7
    '.ni': 'inform7',
    # INI
    '.ini': 'ini',
    # IRPF90
    '.irpf90': 'irpf90',
    # ISBL
    '.isbl': 'isbl',
    # Java
    '.java': 'java',
    # JavaScript
    '.js': 'javascript',
    '.mjs': 'javascript',
    # JBoss CLI
    '.cli': 'jboss-cli',
    # JSON
    '.json': 'json',
    # Julia
    '.jl': 'julia',
    # Julia REPL (if needed)
    '.julia-repl': 'julia-repl',
    # Kotlin
    '.kt': 'kotlin',
    '.kts': 'kotlin',
    # Lasso
    '.lasso': 'lasso',
    # LaTeX
    '.tex': 'latex',
    '.latex': 'latex',
    # LDIF
    '.ldif': 'ldif',
    # Leaf
    '.leaf': 'leaf',
    # LESS
    '.less': 'less',
    # Lisp
    '.lisp': 'lisp',
    '.lsp': 'lisp',
    # LiveCode Server
    '.livecodeserver': 'livecodeserver',
    # LiveScript
    '.ls': 'livescript',
    # LLVM
    '.ll': 'llvm',
    # LSL
    '.lsl': 'lsl',
    # Lua
    '.lua': 'lua',
    # Makefile (by filename; you might handle this specially)
    '.mk': 'makefile',
    '.mak': 'makefile',
    # Markdown
    '.md': 'markdown',
    '.markdown': 'markdown',
    # Mathematica
    '.nb': 'mathematica',
    # MATLAB
    '.m': 'matlab',  # Ambiguous with Objective-C; adjust if needed.
    # Maxima
    '.max': 'maxima',
    # MEL
    '.mel': 'mel',
    # Mercury
    '.mrc': 'mercury',
    # MIPS Assembly
    '.s': 'mipsasm',
    # Mizar
    '.miz': 'mizar',
    # Mojolicious (no standard extension; may be handled by filename)
    # Monkey
    '.monkey': 'monkey',
    # MoonScript
    '.moon': 'moonscript',
    # N1QL
    '.n1ql': 'n1ql',
    # Nginx
    '.nginx': 'nginx',
    # Nim
    '.nim': 'nim',
    # Node REPL
    '.node': 'node-repl',
    # NSIS
    '.nsi': 'nsis',
    '.nsh': 'nsis',
    # Objective-C
    '.mpp': 'objectivec',  # sometimes .mm is used for Objective-C++
    '.mm': 'objectivec',
    '.objc': 'objectivec',
    # OCaml
    '.ml': 'ocaml',
    '.mli': 'ocaml',
    # OpenSCAD
    '.scad': 'openscad',
    # Oxygene
    '.oxygene': 'oxygene',
    # Parser3
    '.parser3': 'parser3',
    # Perl
    '.pl': 'perl',
    '.pm': 'perl',
    # PF
    '.pf': 'pf',
    # PHP
    '.php': 'php',
    '.phtml': 'php',
    # Plaintext (if needed; usually untagged)
    # Pony
    '.pony': 'pony',
    # PowerShell
    '.ps1': 'powershell',
    '.psm1': 'powershell',
    # Processing
    '.pde': 'processing',
    # Profile
    '.profile': 'profile',
    # Prolog
    '.pro': 'prolog',
    # Protocol Buffers
    '.proto': 'protobuf',
    # Puppet
    '.pp': 'puppet',
    # PureBasic
    '.pb': 'purebasic',
    # Python
    '.py': 'python',
    '.pyw': 'python',
    # Q (for kdb+)
    '.q': 'q',
    # QML
    '.qml': 'qml',
    # R
    '.r': 'r',
    '.R': 'r',
    # ReasonML
    '.re': 'reasonml',
    '.rei': 'reasonml',
    # Rib
    '.rib': 'rib',
    # Roboconf (no standard extension; adjust if needed)
    # RouterOS
    '.rsc': 'routeros',
    # RSL
    '.rsl': 'rsl',
    # Ruby
    '.rb': 'ruby',
    '.ru': 'ruby',
    # Rules Language
    '.rules': 'ruleslanguage',
    # Rust
    '.rs': 'rust',
    # SAS
    '.sas': 'sas',
    # Scala
    '.scala': 'scala',
    '.sc': 'scala',
    # Scheme
    '.scm': 'scheme',
    '.ss': 'scheme',
    # Scilab
    '.sci': 'scilab',
    '.sce': 'scilab',
    # SCSS
    '.scss': 'scss',
    # Shell (already covered by .sh)
    # Smali
    '.smali': 'smali',
    # Smalltalk
    '.st': 'smalltalk',
    # SML
    '.sml': 'sml',
    # SQF
    '.sqf': 'sqf',
    # SQL
    '.sql': 'sql',
    # Stan
    '.stan': 'stan',
    # Stata
    '.do': 'stata',
    '.ado': 'stata',
    # STEP (ISO 10303-21)
    '.step': 'step21',
    '.stp': 'step21',
    # Stylus
    '.styl': 'stylus',
    # Subunit
    '.subunit': 'subunit',
    # Svelte
    '.svelte': 'svelte',
    # Swift
    '.swift': 'swift',
    # Taggerscript
    '.tag': 'taggerscript',
    # TAP
    '.tap': 'tap',
    # Tcl
    '.tcl': 'tcl',
    # TeX
    '.tex': 'tex',
    # Thrift
    '.thrift': 'thrift',
    # TP
    '.tp': 'tp',
    # Twig
    '.twig': 'twig',
    # TypeScript
    '.ts': 'typescript',
    '.tsx': 'tsx',
    # Vala
    '.vala': 'vala',
    # VB.NET
    '.vb': 'vbnet',
    '.vbnet': 'vbnet',
    # VBScript
    '.vbs': 'vbscript',
    # VHDL
    '.vhd': 'vhdl',
    '.vhdl': 'vhdl',
    # Vim script
    '.vim': 'vim',
    # x86 Assembly
    '.x86asm': 'x86asm',
    # XL (Excel formulas, etc.)
    '.xl': 'xl',
    # XML
    '.xml': 'xml',
    # XQuery
    '.xq': 'xquery',
    '.xquery': 'xquery',
    # YAML
    '.yaml': 'yaml',
    '.yml': 'yaml',
    # Zephir
    '.zep': 'zephir',
    '.zephir': 'zephir'
}
