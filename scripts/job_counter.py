from pypdf import PdfReader
from collections import Counter


reader = PdfReader("wetransfer_adresboeken-laatste_2024-10-07_1513/1769_19525-1964.pdf") # Read the pdf
page = reader.pages[184] # Pick a page from the pdf
text = page.extract_text() # Extract the text from the page

# Added spaces around newline characters and replace some other characters
text = text.replace("\n", " \n ")
text = text.replace("..", ".,")
text = text.replace("\n", "")
text = text.replace("-  ", "")
text = text.replace("\xad", "")

text_list = text.split("   ") # Split the text on three spaces

text_strip = [sentence.strip() for sentence in text_list] # Remove the excess spaces around the sentence and add the sentence to a list

# List that can be used to determine if a phrase is a street etc.
address_list = ["str", "laan", "weg", "singel", "diep", "w.", "s.", "k.", "kade"]

job_list = [] # The list of jobs mentioned on the page

for sentence in text_strip:
	splits = sentence.split(",") # Split the sentence on commas
	if sentence[0][0] == "-": # Determine if the first character of the sentence is "-"
		job_index = 1 # If the sentence starts with "-", the job is often the second phrase of the sentence
	else:
		job_index = 2 # Job is often the third phrase of the sentence, due to full names of the people
	
	if len(splits) > job_index: # Prevent index out of range
		job = splits[job_index] # Extract the job phrase
		job = job.strip(" ") # Remove the spaces on both sides of the phrase
		if len(job) > 3: # Sometimes "van" or "der" or at the index of the ob, so we exclude those
			if any(char.isdigit() for char in job) == False: # Check if picked phrase does not contain a number, otherwise is could be a street
				if any(substring in job for substring in address_list): # Check if the phrase contains a clue that it still is a street, if not add to job list
					if job[0].isupper() == False: # Check if the first letter of the phrase is not uppercase, otherwise it is a street
						job_list.append(job) # Add the job phrase to the list of jobs
				else:
					job_list.append(job)

job_dict = dict(Counter(job_list)) # Count the unique jobs a make a dictionary where key is job and value is count
print(job_dict)