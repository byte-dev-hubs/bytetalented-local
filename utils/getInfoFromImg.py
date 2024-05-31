import cv2
import pytesseract
import re
from tkinter import filedialog
from tkinter import Tk
import os

def extract_info_from_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # TODO: Use OpenCV to find and crop the avatar from the image

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(img)

    # The first line is the name
    lines = text.split('\n')
    name = lines[2] if len(lines) > 2 else None

    # Use regular expressions to find email and phone number
    email_regex = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
    phone_regex = r"\+?[0-9 ]{10,15}"

    email = re.search(email_regex, text)
    phone = re.search(phone_regex, text)

    # If an email/phone was found, get the match. Otherwise, set to None.
    email = email.group() if email else None
    phone = phone.group() if phone else None

    info = {
        "name": name,
        "email": email,
        "phone": phone
    }
    return info

# # Create a Tk root widget
# root = Tk()
# root.withdraw()  # Hide the root widget

# # Show a dialog for selecting multiple files
# file_paths = filedialog.askopenfilenames()

# # Open the output file
# with open('info.txt', 'w') as f:
#     # Process each selected file
#     for file_path in file_paths:
#         info = extract_info_from_image(file_path)
#         # Write the information to the file, followed by a newline
#         f.write(info + '\n')