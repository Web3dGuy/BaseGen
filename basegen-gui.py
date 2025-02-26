import os
import sys
import json
import pathlib
import fnmatch
import threading
import datetime
from typing import List, Optional, Dict, Set, Any

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import pathspec

# Import functionality from basegen.py
from basegen import load_config, load_gitignore_specs, should_include_file, generate_markdown, guess_language

class BaseGenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BaseGen - Codebase Documentation Generator")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # State variables
        self.workspace_path = None
        self.gitignore_spec = None
        self.config_data = load_config()
        self.selected_files = set()  # Stores paths of files to include
        self.excluded_files = set()  # Stores paths of files to explicitly exclude
        self.output_file = "codebase.md"
        self.is_generating = False
        
        # Tree list exclusions
        self.tree_exclusions = [
            "node_modules",
            ".git",
            ".svn",
            ".hg",
            "__pycache__",
            ".venv",
            "venv",
            "env",
            "dist",
            "build",
            ".cache",
            ".pytest_cache"
        ]
        self.file_exclusions = [
            "*.lock",
            "package-lock.json",
            "yarn.lock",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "*.so",
            "*.dylib",
            "*.dll"
        ]
        
        # Create the main layout
        self.create_menu()
        self.create_main_layout()
        
        # Set up theme
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=25)
        self.style.map('Treeview', background=[('selected', '#3366cc')])
        
        # Initial status
        self.update_status("Welcome to BaseGen. Open a workspace to start.")
    
    def create_menu(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Workspace", command=self.open_workspace)
        file_menu.add_command(label="Save Configuration", command=self.save_configuration, state=tk.DISABLED)
        file_menu.add_command(label="Manage Tree Exclusions", 
                     command=self.manage_tree_exclusions, 
                     state=tk.DISABLED)
        file_menu.add_command(label="Load Configuration", command=self.load_configuration)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Generation menu
        gen_menu = tk.Menu(menubar, tearoff=0)
        gen_menu.add_command(label="Generate Markdown", command=self.generate_markdown_wrapper, state=tk.DISABLED)
        gen_menu.add_command(label="Set Output File", command=self.set_output_file, state=tk.DISABLED)
        menubar.add_cascade(label="Generate", menu=gen_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        self.file_menu = file_menu
        self.gen_menu = gen_menu
    
    def create_main_layout(self):
        """Create the main application layout"""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - File tree
        left_frame = ttk.LabelFrame(main_frame, text="Project Files")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Search bar above the tree
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Filter:").pack(side=tk.LEFT, padx=2)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_tree)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Tree buttons
        tree_button_frame = ttk.Frame(left_frame)
        tree_button_frame.pack(fill=tk.X, padx=5, pady=5)
 
        ttk.Button(tree_button_frame, text="Select All", command=self.select_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(tree_button_frame, text="Deselect All", command=self.deselect_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(tree_button_frame, text="Toggle Selected", command=self.toggle_selection).pack(side=tk.LEFT, padx=2)
        ttk.Button(tree_button_frame, text="Expand All", command=self.expand_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(tree_button_frame, text="Collapse All", command=self.collapse_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(tree_button_frame, text="Refresh", command=self.refresh_tree).pack(side=tk.LEFT, padx=2)
        
        # Create file tree with scrollbar
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.file_tree = ttk.Treeview(tree_frame, selectmode="browse")
        self.file_tree.heading("#0", text="Files", anchor=tk.W)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.file_tree.yview)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Handle file tree events
        self.file_tree.bind("<Double-1>", self.on_tree_double_click)
        self.file_tree.bind("<space>", self.on_tree_space)
        self.file_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Right panel - Configuration and options
        right_frame = ttk.Frame(main_frame, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        right_frame.pack_propagate(False)  
        
        # Options panel
        options_frame = ttk.LabelFrame(right_frame, text="Options")
        options_frame.pack(fill=tk.X, pady=5)
        
        # Checkboxes for options
        self.respect_gitignore_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Respect .gitignore rules", 
                        variable=self.respect_gitignore_var, 
                        command=self.toggle_gitignore).pack(anchor=tk.W, padx=10, pady=5)
        
        self.use_hardcoded_excludes_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Use hardcoded exclusions from config", 
                        variable=self.use_hardcoded_excludes_var, 
                        command=self.toggle_hardcoded_excludes).pack(anchor=tk.W, padx=10, pady=5)
        
        self.add_toc_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Add table of contents", 
                        variable=self.add_toc_var,
                        command=self.update_toc_options).pack(anchor=tk.W, padx=10, pady=5)
        
        self.add_dir_structure_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Add directory structure", 
                        variable=self.add_dir_structure_var,
                        command=self.update_toc_options).pack(anchor=tk.W, padx=10, pady=5)

        self.combined_toc_dir_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Combined TOC/DIR structure", 
                        variable=self.combined_toc_dir_var,
                        command=self.update_toc_options).pack(anchor=tk.W, padx=10, pady=5)
        
        self.compact_tree_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Compact tree view (omit empty dirs)", 
                        variable=self.compact_tree_var).pack(anchor=tk.W, padx=10, pady=5)
                        
        self.add_file_stats_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Add file statistics (lines, size)", 
                        variable=self.add_file_stats_var).pack(anchor=tk.W, padx=10, pady=5)
        
        # Exclusion patterns frame
        exclusion_frame = ttk.LabelFrame(right_frame, text="Exclusion Patterns")
        exclusion_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Exclusion pattern list with add/remove buttons
        button_frame = ttk.Frame(exclusion_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add Pattern", command=self.add_exclude_pattern).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_exclude_pattern).pack(side=tk.LEFT, padx=2)
        
        # Listbox for exclusion patterns with scrollbar
        patterns_frame = ttk.Frame(exclusion_frame)
        patterns_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.exclusion_patterns = tk.Listbox(patterns_frame)
        self.exclusion_patterns.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        patterns_scrollbar = ttk.Scrollbar(patterns_frame, orient="vertical", command=self.exclusion_patterns.yview)
        patterns_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.exclusion_patterns.configure(yscrollcommand=patterns_scrollbar.set)
        
        # Status bar at the bottom
        self.statusbar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, mode='indeterminate')
        self.progress.pack(side=tk.BOTTOM, fill=tk.X, before=self.statusbar)
        self.progress.pack_forget()  # Hide initially
    
    def on_tree_select(self, event):
        """Handle tree item selection"""
        # This is a placeholder for future functionality
        # Such as showing file details in a side panel
        pass
    
    def open_workspace(self):
        """Open a workspace directory"""
        directory = filedialog.askdirectory(title="Select Workspace Directory")
        if directory:
            self.workspace_path = pathlib.Path(directory)
            self.update_status(f"Workspace: {self.workspace_path}")
            
            # Enable menu items
            self.file_menu.entryconfig("Save Configuration", state=tk.NORMAL)
            self.file_menu.entryconfig("Manage Tree Exclusions", state=tk.NORMAL)  # Enable the exclusions menu
            self.gen_menu.entryconfig("Generate Markdown", state=tk.NORMAL)
            self.gen_menu.entryconfig("Set Output File", state=tk.NORMAL)
            
            # Set default output file path
            self.output_file = os.path.join(directory, "codebase.md")
            
            # Load gitignore if present and requested
            if self.respect_gitignore_var.get():
                self.gitignore_spec = load_gitignore_specs(self.workspace_path)
            else:
                self.gitignore_spec = None
            
            # Populate the tree
            self.populate_file_tree()
            
            # Load exclusion patterns from config
            self.load_exclusion_patterns()
    
    def load_exclusion_patterns(self):
        """Load exclusion patterns from config into the listbox"""
        self.exclusion_patterns.delete(0, tk.END)
        if self.use_hardcoded_excludes_var.get() and "HARD_CODED_EXCLUDES" in self.config_data:
            for pattern in self.config_data["HARD_CODED_EXCLUDES"]:
                self.exclusion_patterns.insert(tk.END, pattern)
    
    def toggle_gitignore(self):
        """Toggle respecting gitignore rules"""
        if self.workspace_path:
            if self.respect_gitignore_var.get():
                self.gitignore_spec = load_gitignore_specs(self.workspace_path)
            else:
                self.gitignore_spec = None
            
            # Refresh the tree
            self.populate_file_tree()
    
    def toggle_hardcoded_excludes(self):
        """Toggle using hardcoded exclusions from config"""
        self.load_exclusion_patterns()
    
    def set_output_file(self):
        """Set the output Markdown file path"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialdir=self.workspace_path,
            initialfile="codebase.md",
            title="Save Markdown As"
        )
        if file_path:
            self.output_file = file_path
            self.update_status(f"Output file set to: {self.output_file}")


    def update_toc_options(self):
        """Update TOC and directory structure options based on combined option"""
        if self.combined_toc_dir_var.get():
            # Disable individual options when combined option is selected
            self.add_dir_structure_var.set(True)
            self.add_toc_var.set(True)
            
            # Find the checkbuttons and disable them
            for child in self.root.winfo_children():
                self._disable_checkbuttons_recursive(child, ["Add directory structure", "Add table of contents"])
        else:
            # Re-enable individual options
            for child in self.root.winfo_children():
                self._enable_checkbuttons_recursive(child, ["Add directory structure", "Add table of contents"])
                
    def _disable_checkbuttons_recursive(self, widget, text_list):
        """Recursively find and disable checkbuttons with specific text"""
        if isinstance(widget, ttk.Checkbutton):
            # Get the text option from the checkbutton if possible
            try:
                text = widget.cget("text")
                if text in text_list:
                    widget.configure(state="disabled")
            except:
                pass
        
        # Process children
        try:
            for child in widget.winfo_children():
                self._disable_checkbuttons_recursive(child, text_list)
        except:
            pass

    def _enable_checkbuttons_recursive(self, widget, text_list):
        """Recursively find and enable checkbuttons with specific text"""
        if isinstance(widget, ttk.Checkbutton):
            # Get the text option from the checkbutton if possible
            try:
                text = widget.cget("text")
                if text in text_list:
                    widget.configure(state="normal")
            except:
                pass
        
        # Process children
        try:
            for child in widget.winfo_children():
                self._enable_checkbuttons_recursive(child, text_list)
        except:
            pass

    def save_configuration(self):
        """Save the current configuration to a file"""
        # Collect patterns from the listbox
        patterns = list(self.exclusion_patterns.get(0, tk.END))
        
        config = {
            "workspace": str(self.workspace_path),
            "output_file": self.output_file,
            "respect_gitignore": self.respect_gitignore_var.get(),
            "use_hardcoded_excludes": self.use_hardcoded_excludes_var.get(),
            "add_toc": self.add_toc_var.get(),
            "add_dir_structure": self.add_dir_structure_var.get(),  # New option
            "combined_toc_dir": self.combined_toc_dir_var.get(),    # New option
            "compact_tree": self.compact_tree_var.get(),
            "add_file_stats": self.add_file_stats_var.get(),
            "exclusion_patterns": patterns,
            "selected_files": list(self.selected_files),
            "excluded_files": list(self.excluded_files),
            "tree_exclusions": self.tree_exclusions,
            "file_exclusions": self.file_exclusions
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=self.workspace_path,
            initialfile="basegen_config.json",
            title="Save Configuration As"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
                self.update_status(f"Configuration saved to: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save configuration: {e}")

    def load_configuration(self):
        """Load configuration from a file"""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=self.workspace_path if self.workspace_path else None,
            title="Load Configuration"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Load workspace if specified
                if "workspace" in config:
                    workspace_path = pathlib.Path(config["workspace"])
                    if workspace_path.exists():
                        self.workspace_path = workspace_path
                        
                        # Enable menu items
                        self.file_menu.entryconfig("Save Configuration", state=tk.NORMAL)
                        self.file_menu.entryconfig("Manage Tree Exclusions", state=tk.NORMAL)
                        self.gen_menu.entryconfig("Generate Markdown", state=tk.NORMAL)
                        self.gen_menu.entryconfig("Set Output File", state=tk.NORMAL)
                    else:
                        messagebox.showwarning("Warning", f"Workspace path '{workspace_path}' does not exist.")
                
                # Load output file
                if "output_file" in config:
                    self.output_file = config["output_file"]
                
                # Load options
                if "respect_gitignore" in config:
                    self.respect_gitignore_var.set(config["respect_gitignore"])
                
                if "use_hardcoded_excludes" in config:
                    self.use_hardcoded_excludes_var.set(config["use_hardcoded_excludes"])
                    
                if "add_toc" in config:
                    self.add_toc_var.set(config["add_toc"])
                    
                # Handle new options
                if "add_dir_structure" in config:
                    self.add_dir_structure_var.set(config["add_dir_structure"])
                    
                if "combined_toc_dir" in config:
                    self.combined_toc_dir_var.set(config["combined_toc_dir"])
                    
                # For backward compatibility with old config files
                # that might have the removed 'add_navigation' option
                # We simply ignore it
                    
                if "compact_tree" in config:
                    self.compact_tree_var.set(config["compact_tree"])
                    
                if "add_file_stats" in config:
                    self.add_file_stats_var.set(config["add_file_stats"])
                
                # Update UI state based on combined option
                self.update_toc_options()
                
                # Load exclusion patterns
                if "exclusion_patterns" in config:
                    self.exclusion_patterns.delete(0, tk.END)
                    for pattern in config["exclusion_patterns"]:
                        self.exclusion_patterns.insert(tk.END, pattern)
                
                # Load tree and file exclusions
                if "tree_exclusions" in config:
                    self.tree_exclusions = config["tree_exclusions"]
                    
                if "file_exclusions" in config:
                    self.file_exclusions = config["file_exclusions"]
                
                # Load selected and excluded files if we have a workspace
                if self.workspace_path:
                    # Load gitignore if needed
                    if self.respect_gitignore_var.get():
                        self.gitignore_spec = load_gitignore_specs(self.workspace_path)
                    else:
                        self.gitignore_spec = None
                    
                    # Populate the tree
                    self.populate_file_tree()
                    
                    # Restore selection state
                    if "selected_files" in config:
                        self.selected_files = set(config["selected_files"])
                    
                    if "excluded_files" in config:
                        self.excluded_files = set(config["excluded_files"])
                    
                    # Update UI to reflect selections
                    self._update_tree_selections()
                
                self.update_status(f"Configuration loaded from: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load configuration: {e}")

    # Add method to update tree selections based on loaded configuration
    def _update_tree_selections(self):
        """Update tree item selections based on loaded configuration"""
        def update_item(item_id):
            values = self.file_tree.item(item_id, "values")
            if not values:
                return
                
            path = values[1]
            if path in self.selected_files:
                self.file_tree.item(item_id, values=(values[0], path, "checked"))
                self.file_tree.item(item_id, tags=("checked",))
            elif path in self.excluded_files:
                self.file_tree.item(item_id, values=(values[0], path, "unchecked"))
                self.file_tree.item(item_id, tags=("unchecked",))
            
            # Process children
            for child_id in self.file_tree.get_children(item_id):
                update_item(child_id)
        
        # Start with root items
        for item_id in self.file_tree.get_children():
            update_item(item_id)
        
    def generate_markdown_wrapper(self):
        """Wrapper for generate_markdown to run in a thread"""
        if self.is_generating:
            messagebox.showinfo("Generation in Progress", "Markdown generation is already running.")
            return
        
        # Start the generation thread
        self.is_generating = True
        self.progress.pack(before=self.statusbar)
        self.progress.start()
        self.update_status("Generating Markdown...")
        
        threading.Thread(target=self._generate_markdown_thread, daemon=True).start()
    
    def _generate_markdown_thread(self):
        """Thread worker for Markdown generation"""
        try:
            # Prepare the include/exclude lists from selected files
            include_patterns = []
            
            # Convert selected files to patterns
            for file_path in self.selected_files:
                path = pathlib.Path(file_path)
                if path.is_dir():
                    include_patterns.append(f"{path.name}/**/*")
                else:
                    include_patterns.append(path.name)
            
            # Get patterns from exclusion listbox
            exclude_patterns = list(self.exclusion_patterns.get(0, tk.END))
            
            # Determine options for enhanced markdown generation
            add_toc = self.add_toc_var.get()
            add_dir_structure = self.add_dir_structure_var.get()
            combined_toc_dir = self.combined_toc_dir_var.get()
            compact_tree = self.compact_tree_var.get()
            add_file_stats = self.add_file_stats_var.get()
            
            # Custom extension to generate_markdown with additional features
            self._enhanced_generate_markdown(
                self.workspace_path,
                self.output_file,
                include_patterns,
                exclude_patterns,
                self.gitignore_spec,
                add_toc,
                add_dir_structure,
                combined_toc_dir,
                compact_tree,
                add_file_stats
            )
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.update_status(f"Markdown generated: {self.output_file}"))
            self.root.after(0, self._finish_generation)
        except Exception as e:
            error_msg = f"Error generating Markdown: {e}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            self.root.after(0, lambda: self.update_status(error_msg))
            self.root.after(0, self._finish_generation)
    
    def _finish_generation(self):
        """Finish the generation process"""
        self.progress.stop()
        self.progress.pack_forget()
        self.is_generating = False
        
        # Ask if the user wants to open the file
        if messagebox.askyesno("Generation Complete", 
                              f"Markdown file has been generated at:\n{self.output_file}\n\nWould you like to open it?"):
            self._open_file(self.output_file)
    
    def _open_file(self, path):
        """Open a file with the default system application"""
        try:
            import subprocess
            
            if os.name == 'nt':  # Windows
                os.startfile(path)
            elif os.name == 'posix':  # macOS, Linux
                if sys.platform == 'darwin':  # macOS
                    subprocess.call(('open', path))
                else:  # Linux
                    subprocess.call(('xdg-open', path))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
    
    def _enhanced_generate_markdown(
        self,
        root_path: pathlib.Path,
        output_file: str,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        gitignore_spec: Optional[pathspec.PathSpec] = None,
        add_toc: bool = True,
        add_dir_structure: bool = True,
        combined_toc_dir: bool = False,
        compact_tree: bool = False,
        add_file_stats: bool = False
    ) -> None:
        """
        Enhanced version of generate_markdown with additional features for AI consumption:
        - Optional table of contents with anchor links
        - Optional directory structure representation
        - Combined TOC and directory structure
        - Compact tree view (omitting empty directories)
        - File statistics (lines of code, file size)
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
            raise RuntimeError(f"Error scanning directory '{root_path}': {e}")

        if not included_files:
            raise ValueError("No files found matching the criteria.")

        # Build tree with optional compaction
        if compact_tree:
            tree_dict = self._build_compact_tree(included_files)
        else:
            tree_dict = self._build_tree(included_files)
            
        tree_lines = self._format_tree(tree_dict)
        tree_str = "\n".join(tree_lines)

        md_lines = []
        md_lines.append(f"# Codebase: {root_path.name}")
        md_lines.append("")
        
        # Add metadata for AI consumption
        md_lines.append("## Metadata")
        md_lines.append("")
        md_lines.append(f"- **Generated on:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append(f"- **Files included:** {len(included_files)}")
        if add_file_stats:
            total_loc = 0
            total_size = 0
            for rel_path in included_files:
                file_path = base / rel_path
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            total_loc += len(lines)
                    except UnicodeDecodeError:
                        # Skip binary files for LOC counting
                        pass
                    except Exception:
                        # Skip files with errors
                        pass
                    total_size += file_path.stat().st_size
            
            md_lines.append(f"- **Total lines of code:** {total_loc:,}")
            md_lines.append(f"- **Total size:** {self._format_size(total_size)}")
        md_lines.append("")

# Add combined TOC and directory structure
        if combined_toc_dir:
            md_lines.append("## Project Structure")
            md_lines.append("")
            md_lines.append("```")
            
            # Generate a linked version of the tree
            linked_tree_lines = self._format_linked_tree(tree_dict, "", included_files)
            md_lines.append("\n".join(linked_tree_lines))
            
            md_lines.append("```")
            md_lines.append("")
        else:
            # Add table of contents with anchor links
            if add_toc:
                md_lines.append("## Table of Contents")
                md_lines.append("")
                
                if add_dir_structure:
                    md_lines.append("1. [Directory Structure](#directory-structure)")
                
                md_lines.append(f"{1 if not add_dir_structure else 2}. [Files](#files)")
                
                for i, rel_path in enumerate(included_files):
                    # Create an anchor-friendly ID
                    anchor = f"file-{i+1}"
                    md_lines.append(f"   - [{rel_path}](#{anchor})")
                
                md_lines.append("")

            # Add directory structure as a separate section
            if add_dir_structure:
                md_lines.append("## Directory Structure")
                md_lines.append("")
                md_lines.append("```")
                md_lines.append(tree_str)
                md_lines.append("```")
                md_lines.append("")

        md_lines.append("## Files")
        md_lines.append("")

        for i, rel_path in enumerate(included_files):
            # Create an anchor-friendly ID
            anchor = f"file-{i+1}"
            
            md_lines.append(f"### {rel_path} <a id='{anchor}'></a>")
            md_lines.append("")
            
            if add_file_stats:
                file_path = base / rel_path
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = len(f.readlines())
                        md_lines.append(f"- Lines: {lines}")
                    except UnicodeDecodeError:
                        md_lines.append("- Binary file")
                    except Exception as e:
                        md_lines.append(f"- Error reading file: {e}")
                    
                    md_lines.append(f"- Size: {self._format_size(file_size)}")
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
            
            # Always add navigation links for files
            md_lines.append("")
            if combined_toc_dir:
                md_lines.append("<div style='text-align: right;'><a href='#project-structure'>↑ Back to Project Structure</a></div>")
            elif add_dir_structure:
                md_lines.append("<div style='text-align: right;'><a href='#directory-structure'>↑ Back to Directory Structure</a></div>")
            elif add_toc:
                md_lines.append("<div style='text-align: right;'><a href='#table-of-contents'>↑ Back to Table of Contents</a></div>")
            
            md_lines.append("")

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines))
        except Exception as e:
            raise RuntimeError(f"Error writing to output file '{output_file}': {e}")

    def _format_linked_tree(self, tree, indent, included_files):
        """Format the tree dictionary into a list of strings with linked filenames"""
        lines = []
        for key in sorted(tree.keys()):
            if tree[key]:  # Directory
                lines.append(f"{indent}{key}/")
                lines.extend(self._format_linked_tree(tree[key], indent + "    ", included_files))
            else:  # File
                # Find the index of this file in included_files
                file_path = pathlib.Path(key)
                file_index = None
                
                for i, included_file in enumerate(included_files):
                    if included_file.name == file_path.name:
                        # Check if paths match (considering directory structure)
                        if str(included_file).endswith(str(file_path)):
                            file_index = i + 1
                            break
                
                if file_index is not None:
                    lines.append(f"{indent}[{key}](#file-{file_index})")
                else:
                    lines.append(f"{indent}{key}")
        
        return lines
    
    
    def _build_tree(self, paths: List[pathlib.Path]) -> dict:
        """Build a nested dictionary representing a directory tree"""
        tree = {}
        for path in paths:
            parts = path.parts
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        return tree
    
    def _build_compact_tree(self, paths: List[pathlib.Path]) -> dict:
        """
        Build a compact nested dictionary representing a directory tree,
        collapsing directories with only one child.
        """
        # First, build the full tree
        tree = self._build_tree(paths)
        
        # Then compact it
        return self._compact_tree_node(tree)
    
    def _compact_tree_node(self, node: dict) -> dict:
        """Recursively compact a tree node"""
        # First, compact all children
        for key, child in list(node.items()):
            if child:  # If not a leaf
                node[key] = self._compact_tree_node(child)
        
        # If this node has exactly one child and it's a directory, combine them
        if len(node) == 1:
            key = list(node.keys())[0]
            child = node[key]
            
            # Only combine if the child is a directory
            if child:
                new_node = {}
                for child_key, child_value in child.items():
                    new_key = f"{key}/{child_key}"
                    new_node[new_key] = child_value
                return new_node
        
        return node
    
    def _format_tree(self, tree: dict, indent: str = "") -> List[str]:
        """Format the tree dictionary into a list of strings"""
        lines = []
        for key in sorted(tree.keys()):
            if tree[key]:
                lines.append(f"{indent}{key} >")
                lines.extend(self._format_tree(tree[key], indent + "    "))
            else:
                lines.append(f"{indent}{key}")
        return lines
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in a human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def populate_file_tree(self):
        """Populate the file tree with the workspace directory structure"""
        # Clear the tree
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Clear selections
        self.selected_files = set()
        self.excluded_files = set()
        
        # Start progress bar
        self.progress.pack(before=self.statusbar)
        self.progress.start()
        self.update_status("Loading file tree...")
        
        # Use a thread to avoid UI freezing
        threading.Thread(target=self._populate_tree_thread, daemon=True).start()
    
    def _populate_tree_thread(self):
        """Thread worker for populating the tree"""
        try:
            # Create root node
            root_id = self.file_tree.insert("", "end", text=self.workspace_path.name, open=True, 
                                        values=("directory", str(self.workspace_path), "checked"))
            self.file_tree.item(root_id, tags=("checked",))
            
            # Track which directories we've added
            added_dirs = {self.workspace_path: root_id}
            
            # Add all files to the tree (with performance improvements)
            for path in sorted(self.workspace_path.rglob("*")):
                try:
                    # Skip excluded directories for better performance
                    if any(excluded_dir in path.parts for excluded_dir in self.tree_exclusions):
                        continue
                    
                    # Skip excluded file patterns for better performance
                    if path.is_file() and any(fnmatch.fnmatch(path.name, pattern) for pattern in self.file_exclusions):
                        continue
                        
                    # Get relative path for checking against gitignore
                    rel_path = path.relative_to(self.workspace_path)
                    rel_path_str = str(rel_path).replace(os.sep, "/")
                    
                    # Check if it should be included
                    is_excluded = False
                    if self.gitignore_spec and self.respect_gitignore_var.get():
                        is_excluded = self.gitignore_spec.match_file(rel_path_str)
                    
                    # For directories, we need to ensure the parent path exists in the tree
                    parent_path = path.parent
                    if parent_path not in added_dirs:
                        # Need to build the path
                        self._build_parent_path(parent_path, added_dirs)
                    
                    parent_id = added_dirs[parent_path]
                    
                    # Determine the item properties
                    if path.is_dir():
                        # Create directory item
                        node_id = self.file_tree.insert(parent_id, "end", text=path.name, 
                                                    values=("directory", str(path), "checked" if not is_excluded else "unchecked"))
                        # Track this directory
                        added_dirs[path] = node_id
                        # Add tags for styling
                        if is_excluded:
                            self.file_tree.item(node_id, tags=("unchecked",))
                            self.excluded_files.add(str(path))
                        else:
                            self.file_tree.item(node_id, tags=("checked",))
                            self.selected_files.add(str(path))
                    else:
                        # Create file item
                        node_id = self.file_tree.insert(parent_id, "end", text=path.name, 
                                                    values=("file", str(path), "checked" if not is_excluded else "unchecked"))
                        # Add tags for styling
                        if is_excluded:
                            self.file_tree.item(node_id, tags=("unchecked",))
                            self.excluded_files.add(str(path))
                        else:
                            self.file_tree.item(node_id, tags=("checked",))
                            self.selected_files.add(str(path))
                except Exception as e:
                    print(f"Error adding path to tree: {path} - {e}")
            
            # Configure tags for styling
            self.file_tree.tag_configure("checked", foreground="black")
            self.file_tree.tag_configure("unchecked", foreground="gray")
            
            # Update UI in the main thread
            self.root.after(0, self._finish_tree_loading)
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"Error loading file tree: {e}"))
            self.root.after(0, self.progress.stop)
            self.root.after(0, self.progress.pack_forget)
    
    def manage_tree_exclusions(self):
        """Manage directory and file exclusions for the file tree"""
        exclusion_dialog = tk.Toplevel(self.root)
        exclusion_dialog.title("Manage Tree Exclusions")
        exclusion_dialog.geometry("600x500")
        exclusion_dialog.transient(self.root)
        exclusion_dialog.grab_set()
        
        # Create tabs for directories and files
        notebook = ttk.Notebook(exclusion_dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Directories tab
        dir_frame = ttk.Frame(notebook)
        notebook.add(dir_frame, text="Directory Exclusions")
        
        # Directory list
        dir_frame_top = ttk.Frame(dir_frame)
        dir_frame_top.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        dir_list = tk.Listbox(dir_frame_top)
        dir_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        dir_scrollbar = ttk.Scrollbar(dir_frame_top, orient="vertical", command=dir_list.yview)
        dir_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        dir_list.configure(yscrollcommand=dir_scrollbar.set)
        
        # Populate directory list
        for item in self.tree_exclusions:
            dir_list.insert(tk.END, item)
        
        # Directory buttons
        dir_frame_bottom = ttk.Frame(dir_frame)
        dir_frame_bottom.pack(fill=tk.X, padx=5, pady=5)
        
        def add_dir():
            dir_name = simpledialog.askstring("Add Directory Exclusion", 
                                            "Enter directory name to exclude:", 
                                            parent=exclusion_dialog)
            if dir_name and dir_name not in self.tree_exclusions:
                self.tree_exclusions.append(dir_name)
                dir_list.insert(tk.END, dir_name)
        
        def remove_dir():
            selected = dir_list.curselection()
            if selected:
                idx = selected[0]
                dir_name = dir_list.get(idx)
                self.tree_exclusions.remove(dir_name)
                dir_list.delete(idx)
        
        ttk.Button(dir_frame_bottom, text="Add", command=add_dir).pack(side=tk.LEFT, padx=2)
        ttk.Button(dir_frame_bottom, text="Remove", command=remove_dir).pack(side=tk.LEFT, padx=2)
        
        # Files tab
        file_frame = ttk.Frame(notebook)
        notebook.add(file_frame, text="File Pattern Exclusions")
        
        # File list
        file_frame_top = ttk.Frame(file_frame)
        file_frame_top.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        file_list = tk.Listbox(file_frame_top)
        file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        file_scrollbar = ttk.Scrollbar(file_frame_top, orient="vertical", command=file_list.yview)
        file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        file_list.configure(yscrollcommand=file_scrollbar.set)
        
        # Populate file list
        for item in self.file_exclusions:
            file_list.insert(tk.END, item)
        
        # File buttons
        file_frame_bottom = ttk.Frame(file_frame)
        file_frame_bottom.pack(fill=tk.X, padx=5, pady=5)
        
        def add_file():
            file_pattern = simpledialog.askstring("Add File Pattern Exclusion", 
                                                "Enter file pattern to exclude (e.g. *.lock):", 
                                                parent=exclusion_dialog)
            if file_pattern and file_pattern not in self.file_exclusions:
                self.file_exclusions.append(file_pattern)
                file_list.insert(tk.END, file_pattern)
        
        def remove_file():
            selected = file_list.curselection()
            if selected:
                idx = selected[0]
                file_pattern = file_list.get(idx)
                self.file_exclusions.remove(file_pattern)
                file_list.delete(idx)
        
        ttk.Button(file_frame_bottom, text="Add", command=add_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame_bottom, text="Remove", command=remove_file).pack(side=tk.LEFT, padx=2)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(exclusion_dialog)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def on_ok():
            exclusion_dialog.destroy()
            if self.workspace_path:
                # Refresh the tree with new exclusions
                self.populate_file_tree()
        
        ttk.Button(bottom_frame, text="OK", command=on_ok).pack(side=tk.RIGHT, padx=2)
        ttk.Button(bottom_frame, text="Cancel", command=exclusion_dialog.destroy).pack(side=tk.RIGHT, padx=2)
    
    def _build_parent_path(self, path, added_dirs):
        """Recursively build parent path in the tree"""
        if path in added_dirs:
            return
        
        # Need to build the parent of this path first
        if path.parent != path:  # Not at root
            self._build_parent_path(path.parent, added_dirs)
        
        # Get the parent ID
        parent_id = added_dirs.get(path.parent)
        
        # Create this directory
        is_excluded = False
        if self.workspace_path in path.parents or path == self.workspace_path:
            rel_path = path.relative_to(self.workspace_path)
            rel_path_str = str(rel_path).replace(os.sep, "/")
            if self.gitignore_spec and self.respect_gitignore_var.get():
                is_excluded = self.gitignore_spec.match_file(rel_path_str)
        
        node_id = self.file_tree.insert(parent_id, "end", text=path.name, 
                                      values=("directory", str(path), "checked" if not is_excluded else "unchecked"))
        
        # Track this directory
        added_dirs[path] = node_id
        
        # Add tags
        if is_excluded:
            self.file_tree.item(node_id, tags=("unchecked",))
            self.excluded_files.add(str(path))
        else:
            self.file_tree.item(node_id, tags=("checked",))
            self.selected_files.add(str(path))
    
    def _finish_tree_loading(self):
        """Finish the tree loading process"""
        self.progress.stop()
        self.progress.pack_forget()
        self.update_status(f"Workspace loaded: {self.workspace_path.name}")
    
    def on_tree_double_click(self, event):
        """Handle double click on tree item"""
        item_id = self.file_tree.identify("item", event.x, event.y)
        if item_id:
            values = self.file_tree.item(item_id, "values")
            if values and values[0] == "file":
                path = values[1]
                self.preview_file(path)
    
    def on_tree_space(self, event):
        """Handle space key press on tree item"""
        item_id = self.file_tree.focus()
        if item_id:
            self.toggle_item_selection(item_id)
    
    def toggle_item_selection(self, item_id):
        """Toggle selection state of a tree item"""
        values = self.file_tree.item(item_id, "values")
        if not values:
            return
            
        path = values[1]
        current_state = values[2]
        
        new_state = "checked" if current_state == "unchecked" else "unchecked"
        self.file_tree.item(item_id, values=(values[0], path, new_state))
        
        # Update the tag for styling
        self.file_tree.item(item_id, tags=(new_state,))
        
        # Update our tracking sets
        if new_state == "checked":
            self.selected_files.add(path)
            if path in self.excluded_files:
                self.excluded_files.remove(path)
        else:
            if path in self.selected_files:
                self.selected_files.remove(path)
            self.excluded_files.add(path)
        
        # If it's a directory, update all children
        if values[0] == "directory":
            self._toggle_children(item_id, new_state)
    
    def _toggle_children(self, parent_id, state):
        """Toggle all children of a parent item to the given state"""
        for child_id in self.file_tree.get_children(parent_id):
            values = self.file_tree.item(child_id, "values")
            if not values:
                continue
                
            path = values[1]
            
            # Update this child
            self.file_tree.item(child_id, values=(values[0], path, state))
            self.file_tree.item(child_id, tags=(state,))
            
            # Update tracking sets
            if state == "checked":
                self.selected_files.add(path)
                if path in self.excluded_files:
                    self.excluded_files.remove(path)
            else:
                if path in self.selected_files:
                    self.selected_files.remove(path)
                self.excluded_files.add(path)
            
            # Recurse if this is a directory
            if values[0] == "directory":
                self._toggle_children(child_id, state)
    
    def preview_file(self, path):
        """Preview a file's contents"""
        try:
            file_path = pathlib.Path(path)
            
            # Create a new window for preview
            preview = tk.Toplevel(self.root)
            preview.title(f"Preview: {file_path.name}")
            preview.geometry("800x600")
            
            # Add a text widget with scrollbar
            text_frame = ttk.Frame(preview)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD)
            text.pack(fill=tk.BOTH, expand=True)
            
            # Try to determine language for syntax highlighting
            ext = file_path.suffix
            try:
                # Read the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                text.insert(tk.END, content)
            except UnicodeDecodeError:
                text.insert(tk.END, "Binary file content cannot be displayed.")
            except Exception as e:
                text.insert(tk.END, f"Error reading file: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not preview file: {e}")
    
    def select_all(self):
        """Select all files in the tree"""
        self._select_all_children("", True)
    
    def deselect_all(self):
        """Deselect all files in the tree"""
        self._select_all_children("", False)
    
    def _select_all_children(self, parent_id, select):
        """Helper to select/deselect all children"""
        for item_id in self.file_tree.get_children(parent_id):
            values = self.file_tree.item(item_id, "values")
            if not values:
                continue
                
            path = values[1]
            
            # Set the state
            state = "checked" if select else "unchecked"
            self.file_tree.item(item_id, values=(values[0], path, state))
            self.file_tree.item(item_id, tags=(state,))
            
            # Update tracking sets
            if select:
                self.selected_files.add(path)
                if path in self.excluded_files:
                    self.excluded_files.remove(path)
            else:
                if path in self.selected_files:
                    self.selected_files.remove(path)
                self.excluded_files.add(path)
            
            # Recurse if this is a directory
            if values[0] == "directory":
                self._select_all_children(item_id, select)
    
    def toggle_selection(self):
        """Toggle selection state of the currently selected item(s)"""
        selected_item = self.file_tree.focus()
        if selected_item:
            # Only toggle the currently selected item
            self.toggle_item_selection(selected_item)
    
    def _toggle_selection_children(self, parent_id):
        """Helper to toggle selection of all children"""
        for item_id in self.file_tree.get_children(parent_id):
            values = self.file_tree.item(item_id, "values")
            if not values:
                continue
                
            path = values[1]
            current_state = values[2]
            
            # Toggle the state
            new_state = "checked" if current_state == "unchecked" else "unchecked"
            self.file_tree.item(item_id, values=(values[0], path, new_state))
            self.file_tree.item(item_id, tags=(new_state,))
            
            # Update tracking sets
            if new_state == "checked":
                self.selected_files.add(path)
                if path in self.excluded_files:
                    self.excluded_files.remove(path)
            else:
                if path in self.selected_files:
                    self.selected_files.remove(path)
                self.excluded_files.add(path)
            
            # Recurse if this is a directory
            if values[0] == "directory":
                self._toggle_selection_children(item_id)
    
    def expand_all(self):
        """Expand all nodes in the tree"""
        def _expand_all(parent_id):
            self.file_tree.item(parent_id, open=True)
            for item_id in self.file_tree.get_children(parent_id):
                _expand_all(item_id)
        
        for item_id in self.file_tree.get_children():
            _expand_all(item_id)
    
    def collapse_all(self):
        """Collapse all nodes in the tree"""
        def _collapse_all(parent_id):
            for item_id in self.file_tree.get_children(parent_id):
                _collapse_all(item_id)
            self.file_tree.item(parent_id, open=False)
        
        for item_id in self.file_tree.get_children():
            _collapse_all(item_id)
    
    def refresh_tree(self):
        """Refresh the file tree"""
        if self.workspace_path:
            self.populate_file_tree()
    
    def filter_tree(self, *args):
        """Filter the tree based on search text"""
        search_text = self.search_var.get().lower()
        if not search_text:
            # Show all items
            self._show_all_items()
            return
        
        # Hide all items first
        self._hide_all_items()
        
        # Then show matching items and their parents
        shown_items = set()
        self._show_matching_items("", search_text, shown_items)
    
    def _hide_all_items(self):
        """Hide all items in the tree"""
        def _hide_children(parent_id):
            for item_id in self.file_tree.get_children(parent_id):
                self.file_tree.detach(item_id)  # Detach but don't delete
                _hide_children(item_id)
        
        for item_id in self.file_tree.get_children():
            self.file_tree.detach(item_id)  # Detach but don't delete
            _hide_children(item_id)
    
    def _show_all_items(self):
        """Show all items in the tree"""
        def _restore_children(parent_id, items):
            for item_id in items.get(parent_id, []):
                self.file_tree.move(item_id, parent_id, "end")
                _restore_children(item_id, items)
        
        # Get all items and their parents
        items = self._get_all_detached_items()
        
        # Restore the top-level items
        for item_id in items.get("", []):
            self.file_tree.move(item_id, "", "end")
            _restore_children(item_id, items)
    
    def _get_all_detached_items(self):
        """Get all detached items"""
        detached = {}
        
        def _get_detached(parent_id):
            detached[parent_id] = []
            for item_id in self.file_tree.get_children(parent_id):
                detached[parent_id].append(item_id)
                _get_detached(item_id)
        
        # Initialize with empty root
        detached[""] = []
        
        # Get detached items from hidden storage
        for item_id in self.file_tree.get_children(""):
            detached[""].append(item_id)
            _get_detached(item_id)
        
        return detached
    
    def _show_matching_items(self, parent_id, search_text, shown_items):
        """Show items matching the search text and their parents"""
        has_matching_children = False
        
        for item_id in self.file_tree.get_children(parent_id):
            item_text = self.file_tree.item(item_id, "text").lower()
            values = self.file_tree.item(item_id, "values")
            
            if not values:
                continue
                
            is_match = search_text in item_text
            is_directory = values[0] == "directory"
            
            # Check if any children match
            child_has_match = False
            if is_directory:
                child_has_match = self._show_matching_items(item_id, search_text, shown_items)
            
            # Show this item if it matches or has matching children
            if is_match or child_has_match:
                if item_id not in shown_items:
                    # Make sure the parent is visible
                    parent = self.file_tree.parent(item_id)
                    if parent and parent not in shown_items:
                        self._ensure_parent_visible(parent, shown_items)
                    
                    # Show this item
                    self.file_tree.item(item_id, open=True)  # Expand directories
                    shown_items.add(item_id)
                    
                    # If it's a directory and matches, expand it
                    if is_directory and is_match:
                        self.file_tree.item(item_id, open=True)
                
                has_matching_children = True
        
        return has_matching_children
    
    def _ensure_parent_visible(self, parent_id, shown_items):
        """Ensure a parent item is visible"""
        if not parent_id or parent_id in shown_items:
            return
        
        # Make sure the grandparent is visible
        grandparent = self.file_tree.parent(parent_id)
        if grandparent:
            self._ensure_parent_visible(grandparent, shown_items)
        
        # Show and expand this parent
        self.file_tree.item(parent_id, open=True)
        shown_items.add(parent_id)
    
    def add_exclude_pattern(self):
        """Add a new exclusion pattern"""
        pattern = simpledialog.askstring("Add Exclusion Pattern", "Enter glob pattern to exclude:")
        if pattern:
            self.exclusion_patterns.insert(tk.END, pattern)
    
    def remove_exclude_pattern(self):
        """Remove the selected exclusion pattern"""
        selected = self.exclusion_patterns.curselection()
        if selected:
            self.exclusion_patterns.delete(selected)
    
    def update_status(self, message: str):
        """Update the status bar message"""
        self.statusbar.config(text=message)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About BaseGen",
            "BaseGen - Codebase Documentation Generator\n\n"
            "A tool for generating Markdown documentation from codebases,\n"
            "optimized for AI digestion and analysis.\n\n"
            "Version: 1.0"
        )
    
    def show_docs(self):
        """Show documentation"""
        docs = tk.Toplevel(self.root)
        docs.title("BaseGen Documentation")
        docs.geometry("800x600")
        
        text = scrolledtext.ScrolledText(docs, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add documentation
        text.insert(tk.END, """# BaseGen Documentation

## Overview

BaseGen is a tool for generating Markdown documentation from codebases, optimized for AI digestion and analysis.

## Features

- Select workspace directories for documentation
- Filter files with interactive file tree
- Respect .gitignore rules and patterns
- Add custom exclusion patterns
- Generate Markdown with syntax highlighting
- Add navigation links and table of contents
- Include file statistics
- Compact directory tree view

## Usage

1. **Open Workspace**: Select a directory to document
2. **Select Files**: Check/uncheck files in the tree
3. **Configure Options**: Set options in the right panel
4. **Generate Markdown**: Create the documentation file
5. **Save Configuration**: Save your settings for later use

## Tips for AI Digestion

- Use the "Add table of contents" option for better navigation
- Enable "Add navigation links" for easier jumping between sections
- Include file statistics to provide context about the codebase
- Use the compact tree view for large codebases
- Exclude non-essential files to focus AI analysis

## Command Line Usage

BaseGen can also be used from the command line with the original basegen.py script:

```
python basegen.py <input_dir> -o <output_file> [options]
```

## Keyboard Shortcuts

- **Space**: Toggle file/directory selection
- **Double-click**: Preview file content
""")
        
        text.config(state=tk.DISABLED)  # Make read-only

def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = BaseGenGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
            
            