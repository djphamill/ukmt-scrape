import pytesseract
import requests
from pdf2image import convert_from_bytes
import re

FIRST_YEAR = 2010
FINAL_YEAR = 2010
YEAR_RANGE = range(FIRST_YEAR, FINAL_YEAR + 1)

NUMBER_OF_QUESTIONS = 1
QUESTION_NUMBERS = range(1, NUMBER_OF_QUESTIONS + 1)

BASE_URL = "https://www.colmanweb.co.uk/problemsolving/ukmt"

ANSWERS_REGEX = r"([a-eA-E][ \d]+){4}"

OUTPUT_FILEPATH = '/tmp/output.txt'

def run_extract():
    """ Main workflow of the extract """
    extract = {}
    for year in YEAR_RANGE:
        extract[year] = {}
        for question_number in QUESTION_NUMBERS:
            current_extract = {}
            response = requests.get(f"{BASE_URL}/{year}/{year}.{question_number}.pdf", stream=True)
            [page] = convert_from_bytes(response.content)
            
            image_as_string = pytesseract.image_to_string(page)
            current_extract['image_as_string'] = image_as_string

            question_as_string, answers_as_string, solution_as_string = slice_image(image_as_string)
            if question_as_string and answers_as_string and solution_as_string:
                question = clean_string(question_as_string)
                answers =  clean_string(answers_as_string)
                solution = clean_string(solution_as_string)
            
            if question and answers and solution:
                current_extract.update(dict(question=question, answers=answers, solution=solution))
            
            extract[year][question_number] = current_extract

            write_outputfile(current_extract)


def slice_image(image_as_string):
    """ Find the answers in the image_as_string and return the quesstion and answers"""
    match_objects = [match for match in re.finditer(ANSWERS_REGEX, image_as_string)]
    if len(match_objects) > 1:
        return False, '', '', ''
    beginning_of_answers, end_of_answers = match_objects[0].span()
    question = image_as_string[:beginning_of_answers]
    answers = match_objects[0].group()
    solution = image_as_string[end_of_answers + 1:]
    return question, answers, solution

def clean_string(s):
    """ Remove newline and multiple whitespaces"""
    return s.replace('\n', '').replace('  ', ' ')

def write_outputfile(extract):
    """ Write extract to the output file """

    with open(OUTPUT_FILEPATH, 'a') as f:
        f.write(f"Question: {extract['question']}\n")
        f.write(f"Answers: {extract['answers']}\n")
        f.write(f"Solution: {extract['solution']}\n")


if __name__ == "__main__":
    run_extract()