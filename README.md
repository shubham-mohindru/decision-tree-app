# Decision Tree App

A simple web application that:
- Parses structured text into a decision tree
- Calculates expected values (EV) for each option
- Visualizes the tree using Mermaid.js

## Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Windows: venv\\Scripts\\activate
pip install -r ../requirements.txt
python app.py