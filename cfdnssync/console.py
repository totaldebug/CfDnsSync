from rich.console import Console

from cfdnssync.rich_addons import RichHighlighter

console = Console(highlighter=RichHighlighter())
print = console.print
