from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def analyze_grant_feasibility(grant_data):
    prompt = f"""
You are a UK grant application assistant helping organizations apply for funding from official UK government grants.

Based on the following data, generate a **fully detailed and professional grant application** suitable for submission to the Forestry Commission for the Woodland Creation Planning Grant (WCPG). 

Do **not** leave placeholders like [Business Name] or [Project Title]. Instead, write natural, realistic content as if this is a complete final version.

### Grant Metadata
- Grant Name: {grant_data.get('grantName')}
- Funder: {grant_data.get('grantFunder')}
- Award Range: {grant_data.get('grantMinimumAwardDisplay')} to {grant_data.get('grantMaximumAwardDisplay')}
- Eligible Locations: {', '.join(grant_data.get('grantLocation', []))}
- Eligible Applicant Types: {', '.join(grant_data.get('grantApplicantType', []))}
- Application Open: {grant_data.get('grantApplicationOpenDate')}
- Application Close: {grant_data.get('grantApplicationCloseDate')}
- Description: {grant_data.get('grantShortDescription')}
- Grant URL: {grant_data.get('url')}

### Business Information
- Business Name: {grant_data.get('business_name')}
- Industry: {grant_data.get('business_industry')}
- Contact Name: {grant_data.get('contact_name')}
- Email: {grant_data.get('contact_email')}
- Phone: {grant_data.get('contact_phone')}
- Location: {grant_data.get('contact_state')}

### Project Details
- Project Title: {grant_data.get('project_title')}
- Description: {grant_data.get('project_description')}
- Start Date: {grant_data.get('start_date')}
- Duration (months): {grant_data.get('duration')}
- Funding Amount Requested: £{grant_data.get('funding_amount')}

---

### Output Format

Write the grant application in Markdown-style structure using the following sections:

## Executive Summary  
## Business Overview  
## Project Description  
## Objectives and Deliverables  
## Funding Justification and Budget  
## Timeline and Milestones  
## Expected Impact  
## Sustainability Plan  
## Supporting Evidence (recommendations only)  
## Conclusion

Write in a formal and persuasive tone, as if preparing a real submission to the UK government.
"""



    # Send request to GPT-4
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You help software developers build tools for government grant application automation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()
