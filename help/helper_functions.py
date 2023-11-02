import os
from pathlib import Path
import re
import uuid

def get_data_from_txt(filename: str | Path, transforms: dict = {"\n": " "}) -> str:
    with open(filename, 'r', encoding="utf-8") as f:
        return translate(f.read(), transforms) # Same as str.replace but can handle multiple transforms and works with regex
    
def translate(text, transforms:  dict):
  """Translates text using a regular expression dictionary.

  Args:
    text: The text to translate.
    regex_dict: A dictionary of regular expressions to replacement strings.

  Returns:
    The translated text.
  """

  for regex, replacement in transforms.items():
    text = re.sub(regex, replacement, text)
  return text

# Create a regular expression dictionary to replace anything inside {} with a space.
regex_dict = {
  r"\{([^}]+)\}": "{}"
}

def GenRandomString(length: int = 10) -> str:
    return str(uuid.uuid4())[:length]