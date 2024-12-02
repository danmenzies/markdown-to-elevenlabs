import os
import re
from unidecode import unidecode

class split_markdown:
    """
    Splits a Markdown file into individual sections.
    """

    def __init__(self, PROJECT_ROOT):
        """
        Constructor for split_markdown class.
        :param PROJECT_ROOT:
        """
        self.PROJECT_ROOT = PROJECT_ROOT
        self.source_dir = os.path.join(PROJECT_ROOT, "markdown")
        self.output_dir = os.path.join(PROJECT_ROOT, "output", "markdown")
        self.files_to_process = []

    def main(self, reset):
        """
        Main function to split the Markdown file.
        :param reset: If True, deletes previous output and starts fresh.
        :return:
        """
        # Build the path to the Markdown files
        markdown_dir = os.path.join(self.PROJECT_ROOT, "markdown")
        markdown_files = os.listdir(markdown_dir)
        markdown_files = [f for f in markdown_files if f.endswith(".md")]

        # If reset is True, delete the output directory
        if reset and os.path.exists(self.output_dir):
            os.system(f"rm -rf {self.output_dir}")

        # Loop through the Markdown files
        for markdown_file in markdown_files:
            self.split_file(markdown_file)

    def split_file(self, markdown_file):
        """
        Split a Markdown file into individual sections.
        :param markdown_file: The file to split.
        :return:
        """
        # Create the output directory if it doesn't exist
        single_output_dir = os.path.join(self.output_dir, markdown_file.replace(".md", ""))
        if not os.path.exists(single_output_dir):
            os.makedirs(single_output_dir, exist_ok=True)

        # Read the Markdown file
        try:
            with open(os.path.join(self.source_dir, markdown_file), "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {markdown_file}: {e}")
            return

        # Convert Unicode characters to ASCII
        content = unidecode(content)

        # Preprocessing: Replace unusual characters
        content = content.replace("—", ". ")  # Replace em dash with period and space
        content = content.replace("–", ". ")  # Replace en dash with period and space
        content = content.replace("…", "...")  # Replace ellipsis with three dots
        content = re.sub(r'[“”]', '"', content)  # Replace fancy quotes with straight quotes
        content = re.sub(r"[‘’]", "'", content)  # Replace fancy single quotes with straight quotes
        content = content.replace('"',"")  # Remove double quotes

        # Remove links but keep labels if available, or remove entire link if standalone
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)  # Handles labeled links
        content = re.sub(r'<https?://[^\s>]+>', '', content)  # Handles standalone URLs

        # Strip remaining Markdown formatting (e.g., headers, bold, italic, etc.)
        content = re.sub(r'[#*_~`]', '', content)  # Basic formatting characters
        content = re.sub(r'!\[.*?\]\(.*?\)', '', content)  # Images
        content = re.sub(r'>\s+', '', content)  # Blockquotes
        content = re.sub(r'-{3,}', '', content)  # Horizontal rules

        # Split content into sections by paragraphs or full lists
        sections = re.split(r'(?:\n{2,})', content)  # Splits by double newlines (paragraphs)

        # Process each section
        section_count = 1
        for section in sections:
            section = section.strip()

            # Skip empty sections
            if not section:
                continue

            # Check if the section is a list (starts with `-`, `*`, or digit + period)
            if re.match(r'^(\s*[-*]|\d+\.)', section):
                # Keep full list as one section by appending following list items
                list_items = [section]
                while sections and re.match(r'^(\s*[-*]|\d+\.)', sections[0]):
                    list_items.append(sections.pop(0))
                section = "\n".join(list_items)

            # Additional cleaning: Remove any lingering problematic characters
            section = re.sub(r'[^\x00-\x7F]+', ' ', section)  # Remove non-ASCII characters

            # Write the section to an individual file
            output_file_path = os.path.join(single_output_dir, f"section_{section_count:03}.md")
            with open(output_file_path, "w", encoding="utf-8") as out_file:
                out_file.write(section)
                self.files_to_process.append(output_file_path)

            section_count += 1
