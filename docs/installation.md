---
title: Installation
weight: -5
---

## Prerequisites

Before installing Frame, ensure you have the following prerequisites:

- Python 3.11 or higher
- Git
- Virtual environment tool (optional but recommended)
- Docker (optional)

## Installation Steps

1. **Clone the Repository**

   Clone the Frame repository from GitHub:

   ```bash
   git clone https://github.com/your-repo/frame.git
   cd frame
   ```

2. **Set Up a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Set up necessary environment variables for API keys and other configurations:

   ```bash
   export OPENAI_API_KEY='your-openai-api-key'
   export MISTRAL_API_KEY='your-mistral-api-key'
   export HUGGINGFACE_API_KEY='your-huggingface-api-key'
   ```

5. **Run Tests**

   Ensure everything is set up correctly by running the tests:

   ```bash
   pytest
   ```

## Next Steps

- [[usage]]
- [[api_reference]]
