import google.generativeai as genai
import os
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retries = Retry(
    total=3,
    backoff_factor=1,       # wait: 1s, 2s, 4s...
    status_forcelist=[500, 502, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

api_key = os.environ.get("AI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set GEMINI_API_KEY environment variable.")

# Configure the Gemini API client
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def scrape_url(content: str, queries: list[dict[str, str]], tables: list[dict[str, str]], desc: str) -> list[str]:
    sql_commands = []
    for table in tables:
        table_name = list(table.keys())[0]
        sql = f"INSERT INTO {table_name} ("
        table_queries = []
        for q in queries:
            if list(q.values())[0].startswith(table_name + "."):
                table_queries.append(list(q.keys()[0]))
                sql += list(q.values())[0].split(".")[1] + ","
        sql = sql[:-1]
        sql += ") VALUES"
        prompt = f"""
            This is a description of the general info we want to obtain {desc}
            We now want to add relevant info to the table described using this dictionary that map the different columns
            to their description and constraint 
            '{table.values()}'
            All info should come from this: '{content}'
            
            Complete this insert command and return it as response: {sql}
            these are the different queries you will will use in obtaining data for the attributes: {table_queries}
            if you find nothing return an empty string
        """
        response = model.generate_content(prompt)
        sql = response.text
        sql_commands.append(sql)
    return sql_commands


def get_content(url: str) -> str:
    try:
        response = session.get(url, timeout=10)
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type or response.status_code == 503:
            print(f"{url} URL does not return HTML content OR 503 CODE")
            return ""
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ")
        return text
    except Exception as e:
        print(e)
        return ""




