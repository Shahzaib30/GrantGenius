import os
from openai import OpenAI, RateLimitError, APIError, APIConnectionError
import requests 
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def fetch_website_data(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        return text[:2000]
    except Exception as e:
        return f"Error fetching data from {url}: {str(e)}"
    
def analyze_website(url, model="gpt-4"):
    data = fetch_website_data(url)
    if data.startswith("Error"):
        return {"error": data}
    
    prompt = f"""
You are an assistant analyzing UK business websites to match them with UK government grant opportunities.

Your task is to extract four specific pieces of information from the business. You will first use the provided website content (scraped data). If the required information is incomplete or unclear, you may reason based on the website context and make your best guess. Do not leave any field as "Not specified".

Return the result **in exactly this format**:

Industry: <one clear industry>  
Funding Purpose: <one main purpose>  
Amount Needed: <a GBP range like 0–5000, 5000–10000, etc.>  
Region: <choose one: England, Scotland, Wales, Northern Ireland — do not use any non-UK countries>

Rules:
- Use your judgment to infer missing or unclear information — **always return a plausible value**.
- Only return these four lines, with no explanations or extra text.
- If the business is not clearly UK-based, infer the most likely UK region or default to "England" if necessary.
- Use the website content below as your source of truth.

Website content:
\"\"\"  
{data}  
\"\"\"
"""


    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message.content

    except RateLimitError:
        if model == "gpt-4":
            print("[!] GPT-4 quota exceeded. Falling back to gpt-3.5-turbo.")
            return analyze_website(url, model="gpt-3.5-turbo")
        else:
            return {"error": "Quota exceeded. Please check your OpenAI usage."}
    except (APIConnectionError, APIError) as e:
        return {"error": f"API connection failed: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    



