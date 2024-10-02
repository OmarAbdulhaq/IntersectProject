import PyPDF2
import docx
from openai import OpenAI
import os
import json
import re

os.environ['OPENAI_API_KEY'] = "sk-x68EAydklMlCOWiNvw5sLi_Eo7yuqCc_uVanLyOSUyT3BlbkFJwxaVPOeUv9H9rUCsYGE1RB0ir6PLhmWMf9NXqjBKAA"
client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_entities(text):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an entity extraction system"},
            {"role": "user", "content": f"""Extract the following details from the text, and respond with pure JSON:
            \n\nPersonal Information:
            Name: Usually on top of the page.
            Gender: Extract sex, depending on the name.
            Age: Write exact age if provided, write 'in their 20s' or 'in their 30s' for example depending on the year they went to university.
            
            \nEducation:
            Academic level: Always Bachelors degree, except for if they mention a masters or a doctorate degree.
            Institution: Normally written under the Academic Level indicating the university/collage/institution they studied in.
            GPA/Grade: If mentioned, write it down, otherwise, infer their level of expertise.
            Start date: The date they started studying at that institution, naturally, at the left side of the written range ([Sep 2023] - Jan 2024).
            End date: The date they finsihed studying at that institution, naturally, at the right side of the written range (Sep 2023 - [Jan 2024]).
            
            \nWork Experience:
            Company: The name of the comapny the person worked at.
            Location: If it's written down, use it, otherwise, infer it from the Comapny name (you can search for it online),
            Role: If it's mentioned, write it down, otherwise, infer it from the description.
            Start date: The date they started working at that company, naturally, at the left side of the written range ([Sep 2023] - Jan 2024).
            End date: The date they finsihed working at that company, naturally, at the right side of the written range (Sep 2023 - [Jan 2024]).
            Description: Summarize the description they've written about yourself, highlight most important details.
            \n\n
             {text}"""
            }
        ],        
        max_tokens=1000,
        temperature=0.1
    )

    response = completion.choices[0].message.content.strip()
    cleaned_response = re.sub(r'```json|```', '', response).strip()
    try:
        response_json = json.loads(cleaned_response)
    except json.JSONDecodeError:
        raise ValueError("The response from OpenAI was not valid JSON.")
    
    print(response_json)
    return response_json