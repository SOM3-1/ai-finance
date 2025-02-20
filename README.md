# ai-finance
# Create a virtual environment named 'venv'
python -m venv venv

# On Windows, activate the environment
venv\Scripts\activate

# On macOS/Linux, activate the environment
source venv/bin/activate

pip install -r requirements.txt

uvicorn backend.ai_api:app --host 0.0.0.0 --port 8000 --reload

deactivate
