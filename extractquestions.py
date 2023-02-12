import pytesseract
import requests
from pdf2image import convert_from_bytes
import re

from handleerror import HandleError

FIRST_YEAR = 2010
FINAL_YEAR = 2021
YEAR_RANGE = range(FIRST_YEAR, FINAL_YEAR + 1)

NUMBER_OF_QUESTIONS = 25
QUESTION_NUMBERS = range(1, NUMBER_OF_QUESTIONS + 1)

BASE_URL = "https://www.colmanweb.co.uk/problemsolving/ukmt"

ANSWERS_REGEX = r"([a-eA-E][ \d]+){4}"

OUTPUT_FILEPATH = '/tmp/output.txt'

ERRORS = dict(
    sliced_image='Could not slice image',
    
)

def run_extract():
    """ Main workflow of the extract """
    extract = {}
    for year in YEAR_RANGE:
        print(f'Beginning extract for Year: {year}')
        extract[year] = {}
        for question_number in QUESTION_NUMBERS:
            print(f'Question: {question_number}', end=' ')
            question_dict = {}
            response = requests.get(f"{BASE_URL}/{year}/{year}.{question_number}.pdf", stream=True)
            if not valid_response(response):
                HandleError.RESPONSE_FAILURE(year, question_number, response.content)
                continue
            [page] = convert_from_bytes(response.content)
            
            image_as_string = pytesseract.image_to_string(page)
            question_dict['image_as_string'] = image_as_string

            question_as_string, answers_as_string, solution_as_string = slice_image(image_as_string)
            if question_as_string and answers_as_string and solution_as_string:
                question = clean_string(question_as_string)
                answers =  clean_string(answers_as_string)
                solution = clean_string(solution_as_string)
            else:
                HandleError.CANNOT_SLICED_IMAGE(year, question_number, image_as_string)
                continue
            
            if question and answers and solution:
                question_dict.update(dict(question=question, answers=answers, solution=solution))
            
            extract[year][question_number] = question_dict

            write_outputfile(question_dict)
            print(f'... SUCCESS')

        print(f'Year {year} DONE. TOTAL successful questions extracted: {len(extract[year].keys())}')


def slice_image(image_as_string):
    """ Find the answers in the image_as_string and return the quesstion and answers"""
    match_objects = [match for match in re.finditer(ANSWERS_REGEX, image_as_string)]
    if not match_objects or len(match_objects) > 1:
        return '', '', ''
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

def valid_response(response):
    """ Validate response: return True if valid; otherwise, False."""
    return response.status_code == 200


if __name__ == "__main__":
    run_extract()