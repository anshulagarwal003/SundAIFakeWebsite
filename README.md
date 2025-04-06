# Honeypot Generator

A Python tool that generates deceptive honeypot content for websites using GPT-4 and a Master Control Program (MCP) architecture.

## Features

- MCP Architecture with three specialized agents:
  - Content Agent: Generates deceptive but realistic content
  - Structure Agent: Creates hidden HTML structures
  - Coordination Agent: Reviews and enhances the final output

- Processes HTML files to add hidden honeypot content
- Maintains original website appearance for real users
- Creates bot-detectable traps in the form of hidden forms and content

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Usage

```bash
python generate_honeypot.py
```

This will:
1. Read the input HTML file (default: ./docs/index.html)
2. Generate honeypot content using the MCP system
3. Create a protected version (default: ./docs/protected/index.html)

## Configuration

- Input/output paths can be modified in `generate_honeypot.py`
- Agent instructions can be customized in the MCP class
- Hidden content styling can be adjusted in the HTML output

## Security Notes

- Keep your OpenAI API key secure
- Never commit .env files to version control
- Review generated honeypot content before deployment
