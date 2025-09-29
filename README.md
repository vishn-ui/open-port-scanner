Setup and Installation
Follow these steps to get the analyzer running on your local machine.

1. Clone the Repository
Bash

git clone https://github.com/your-username/ai-phishing-analyzer.git
cd ai-phishing-analyzer
2. Create a requirements.txt file
Create a file named requirements.txt in the project directory and add the following line:

google-generativeai
3. Install Dependencies
Install the necessary Python library using pip:

Bash

pip install -r requirements.txt
4. Get Your Google AI API Key
Visit Google AI Studio.

Click "Get API key" and create one in a new project.

Copy the generated API key.

5. Set Up Your API Key
It's critical to set your API key as an environment variable for security.

On macOS/Linux:

Add the following line to your ~/.zshrc or ~/.bash_profile file to make the key available in all terminal sessions:

Bash

export GOOGLE_API_KEY="PASTE_YOUR_API_KEY_HERE"
Then, reload your terminal or run source ~/.zshrc.

On Windows:

You can set it for the current terminal session with:

Bash

set GOOGLE_API_KEY="PASTE_YOUR_API_KEY_HERE"
## 🚀 Usage
The script runs in an interactive mode, waiting for you to paste the email content.

Run the script from your terminal:

Bash

python ai_analyzer.py
Paste the raw email content into the terminal. This should include the headers (From:, Subject:, etc.) for the most accurate analysis.

Signal the end of input:

On macOS/Linux, press Ctrl + D.

On Windows, press Ctrl + Z, then Enter.

The script will then contact the Gemini API and print the detailed analysis.
