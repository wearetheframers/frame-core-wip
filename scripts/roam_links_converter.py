import re
import os


def should_ignore_file(content):
    """
    Check if the file should be ignored based on the presence of the roam-ignore comment.

    Args:
    content (str): The content of the file.

    Returns:
    bool: True if the file should be ignored, False otherwise.
    """
    return "<!---\nroam-ignore\n-->" in content


def convert_roam_links(content, docs_dir):
    """
    Convert standard Markdown links to roam-style links and generate new roam-style links.

    Args:
    content (str): The content to process.
    docs_dir (str): The directory containing the documentation files.

    Returns:
    str: The processed content with converted and new roam-style links, or the original content if the file should be ignored.
    """
    if should_ignore_file(content):
        return content

    def replace_link(match):
        link_text = match.group(1)
        link_url = match.group(2)

        # If it's an internal link (not starting with http:// or https://)
        if not link_url.startswith(("http://", "https://")):
            file_name = os.path.basename(link_url)
            file_name_without_ext = os.path.splitext(file_name)[0]
            new_link = f"[[{file_name_without_ext}]]"
            return new_link

        return match.group(0)

    # Convert existing Markdown links to roam-style
    pattern = r"\[(.*?)\]\((.*?)\)"
    content = re.sub(pattern, replace_link, content)

    # Remove any extra brackets that might have been added
    content = re.sub(r"\[{2,}", "[[", content)
    content = re.sub(r"\]{2,}", "]]", content)
    return content


# Example usage:
# processed_content = convert_roam_links(original_content, '/path/to/docs')
