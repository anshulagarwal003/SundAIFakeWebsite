import openai
import os
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
import json
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Agent:
    def __init__(self, name: str, role: str, instructions: str):
        self.name = name
        self.role = role
        self.instructions = instructions
        
    def generate_response(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"{self.role}\nInstructions: {self.instructions}"},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']

class MasterControlProgram:
    def __init__(self):
        # Initialize agents with specific instructions
        self.content_agent = Agent(
            "Content Agent",
            "You are a deceptive content generator. Create realistic but fake technical content that matches the style and theme of the input content.",
            "Generate deceptive but realistic technical content that matches the style of the input."
        )
        self.structure_agent = Agent(
            "Structure Agent",
            "You are an HTML structure expert. Create HTML elements that hide content while making it accessible to web scrapers.",
            "Create HTML structures that hide content while keeping it accessible to scrapers."
        )
        self.coordination_agent = Agent(
            "Coordination Agent",
            "You are a honeypot coordinator. Review and combine content to create effective deceptive websites.",
            "Review and enhance the combined content for maximum effectiveness."
        )
    
    def generate_honeypot_content(self, original_content: str) -> str:
        # Step 1: Generate fake content based on original content
        content_prompt = f"Analyze this content and generate additional deceptive but realistic content that matches its style and theme:\n{original_content}"
        fake_content = self.content_agent.generate_response(content_prompt)
        
        # Step 2: Create HTML structure to hide the content
        structure_prompt = f"Create HTML structure to hide this content while keeping it accessible to scrapers. The content should be invisible to users but readable by bots:\n{fake_content}"
        html_structure = self.structure_agent.generate_response(structure_prompt)
        
        # Step 3: Coordinate and finalize
        coordination_prompt = f"Review and enhance this honeypot HTML. Make sure it's well-hidden but detectable by scrapers:\n{html_structure}"
        final_honeypot = self.coordination_agent.generate_response(coordination_prompt)
        
        return final_honeypot

def process_html_file(input_path: str, output_path: str):
    # Create MCP instance
    mcp = MasterControlProgram()
    
    # Read input HTML
    with open(input_path, 'r') as f:
        html_content = f.read()
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Generate honeypot content
    honeypot_content = mcp.generate_honeypot_content(str(soup))
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Insert honeypot content before </body>
    body_tag = soup.find('body')
    if body_tag:
        honeypot_div = soup.new_tag('div')
        honeypot_div['style'] = 'display: none;'
        honeypot_div['class'] = 'seo-content'
        honeypot_div.append(BeautifulSoup(honeypot_content, 'html.parser'))
        body_tag.append(honeypot_div)
    
    # Write to output file
    with open(output_path, 'w') as f:
        f.write(str(soup.prettify()))
    
    print(f"Honeypot content added to {output_path}")

def main():
    # Define input and output paths
    input_path = "./docs/index.html"
    output_path = "./docs/protected/index.html"
    
    # Process the HTML file
    process_html_file(input_path, output_path)

if __name__ == "__main__":
    main()
