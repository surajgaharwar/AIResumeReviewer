# import libraries
from openai import OpenAI
import yaml

api_key = None
CONFIG_PATH = r"config.yaml"

with open(CONFIG_PATH) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    api_key = data['GROQ_API_KEY']   # <-- changed to GROQ_API_KEY

import re

def ats_extractor(resume_data):
    prompt =prompt = '''
You are an AI assistant specialized in parsing and evaluating resumes for job readiness.
Given a resume as input, extract the following fields in **well-formatted JSON** only — no extra text or explanation.

### Extract and return:

1. full_name  
2. email_id  
3. github_portfolio  
4. linkedin_id  
5. employment_details: list of objects, each with "company", "role", and "duration"  
6. technical_skills: list of technologies  
7. soft_skills: list of interpersonal skills  
8. ats_score: A dynamic score out of 100, based on:
   - Relevance and clarity of work experience (30%)
   - Technical skills match to general software roles (25%)
   - Presence of important links (GitHub, LinkedIn) (10%)
   - Formatting, clarity, and completeness (15%)
   - Inclusion of soft skills and communication indicators (10%)
   - Overall structure and professionalism (10%)

### Output Format (strictly follow this structure):

{
  "full_name": "Full Name",
  "email_id": "email@example.com",
  "github_portfolio": "https://github.com/username",
  "linkedin_id": "https://www.linkedin.com/in/username",
  "employment_details": [
    {
      "company": "Company Name",
      "role": "Job Title",
      "duration": "Start Date - End Date"
    }
  ],
  "technical_skills": [
    "Skill 1", "Skill 2", "Skill 3"
  ],
  "soft_skills": [
    "Skill A", "Skill B"
  ],
  "ats_score": ats_score
}

Only respond with the JSON data in the structure above.

'''


    openai_client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )    

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": resume_data}
    ]

    response = openai_client.chat.completions.create(
        model="llama3-70b-8192",  
        messages=messages,
        temperature=0.0,
        max_tokens=1500,
    )
        
    data = response.choices[0].message.content

    # extract only JSON part using regex
    match = re.search(r'\{.*\}', data, re.DOTALL)
    if match:
        json_part = match.group(0)
        return json_part
    else:
        return "{}"   # fallback if something goes wrong
