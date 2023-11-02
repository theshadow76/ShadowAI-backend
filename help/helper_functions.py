import os
from pathlib import Path
import re
import uuid
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

def get_start_end_dates():
    # Get the current time
    start_date = datetime.now()
    
    # Calculate the date one month later
    end_date = start_date + relativedelta(months=+1)
    
    # Format the dates in ISO 8601 format and append 'Z' to indicate UTC time
    start_date_iso = start_date.isoformat() + 'Z'
    end_date_iso = end_date.isoformat() + 'Z'
    
    return start_date_iso, end_date_iso