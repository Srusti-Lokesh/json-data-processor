# JSON Data Processor

A beginner-friendly Python project that reads JSON files and supports searching, filtering, and summarizing structured records. It includes both a command-line processor and a small Flask web interface that can be deployed to Render.

## Features
- Reads employee, product, and student records from JSON files.
- Case-insensitive text search across records.
- Field-based filtering using a substring match.
- Numeric summaries (minimum, maximum, average).
- Input validation and useful error messages for malformed JSON.
- Saves filtered records to an output JSON file from the CLI.
- Responsive browser interface.
- Unit tests for core processing functions.

## Technology
- Python 3
- `json`, `argparse`, `pathlib`, `unittest` standard-library modules
- Flask
- Gunicorn (Render production server)

## Project structure
```text
json_data_processor_project/
├── app.py
├── processor.py
├── requirements.txt
├── render.yaml
├── Procfile
├── README.md
├── data/
│   ├── employees.json
│   ├── products.json
│   └── students.json
└── tests/
    └── test_processor.py
```

## Run locally in Windows PowerShell

1. Install Python 3.10 or newer from the official Python website and select **Add Python to PATH** during installation.
2. Extract the ZIP, open PowerShell, and change to the extracted project directory. Example:
   ```powershell
   cd "$HOME\Downloads\json_data_processor_project"
   ```
   If you extracted it elsewhere, replace the path with your actual folder path.
3. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run this only for the current terminal, then activate again:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Start the web application:
   ```powershell
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser. Use the dataset selector, search box, and field filter.
7. Stop the server with **Ctrl+C** in PowerShell.

## CLI examples (PowerShell)

Search all employee records for Bengaluru:
```powershell
python processor.py --dataset employees --query Bengaluru --summary
```

Filter products by category:
```powershell
python processor.py --dataset products --field category --value Electronics --summary
```

Filter students by course and save the result:
```powershell
python processor.py --dataset students --field course --value Python --output .\python_students.json --summary
```

Use your own JSON file:
```powershell
python processor.py --input .\my_records.json --query Alice --summary
```
Input JSON must be an array of objects, for example:
```json
[
  {"name": "Alice", "department": "Engineering"},
  {"name": "Bob", "department": "Sales"}
]
```

## Run tests
With the virtual environment activated:
```powershell
python -m unittest discover -s tests -v
```

## Deploy to Render

This is a Flask web application, so deploy it as a **Web Service**.

1. Create a GitHub repository and push this project (steps below).
2. Sign in to Render and connect your GitHub account.
3. In Render, choose **New + → Web Service**, then select this repository.
4. Render should detect `render.yaml`; if it asks for settings, use:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Health check path: `/`
5. Select the free instance if available for your account/region, then click **Create Web Service**.
6. Wait for the deployment to finish. Open the `onrender.com` URL shown by Render.
7. Verify all three datasets, search, field filtering, and summary cards.
8. If the deployment fails, open **Logs** in Render. Confirm `requirements.txt` includes Flask, that the start command is `gunicorn app:app`, and that `app.py` contains the Flask object named `app`.
9. After making changes, commit and push them to GitHub; Render can redeploy automatically when auto-deploy is enabled.

Note: Render free-plan availability and limits can change. The app uses bundled sample JSON files; changes made to files on a deployed instance should not be treated as permanent storage.

## GitHub setup using PowerShell

Create an empty repository on GitHub first. Suggested repository name: `json-data-processor`. Do not initialize it with a README, license, or `.gitignore` because this folder already contains project files.

Then, from the project folder:
```powershell
git init
git add .
git commit -m "Build JSON data processor"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/json-data-processor.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. If Git asks you to sign in, complete the browser authentication flow. Do not put passwords or access tokens directly into commands.

Suggested GitHub repository description:
> A Python JSON data processing project with search, field filtering, numeric summaries, sample employee/product/student datasets, a CLI, and a Flask web interface deployable to Render.

Suggested topics: `python`, `json`, `flask`, `data-processing`, `render`, `beginner-project`.

## Submission checklist
- [ ] Test the app locally in PowerShell.
- [ ] Run the unit tests and confirm all pass.
- [ ] Push the full project to a **public** GitHub repository if your internship portal requires public access.
- [ ] Deploy the repository on Render and open the live URL to verify it works.
- [ ] Add the GitHub repository URL and live Render URL to your submission.
- [ ] Include the project report PDF.
- [ ] Capture genuine screenshots of the running app and successful test output if requested.
- [ ] Submit the repository link through the internship portal.
- [ ] Publish a LinkedIn post after deployment, with your actual repository and live-app links.
- [ ] Do not claim tests/deployment passed until you have run and verified them yourself.

## LinkedIn post template

**Project completed: JSON Data Processor | Python**

I built a JSON Data Processor project to practise working with structured data in Python.

**What I implemented**
- Read JSON records for employees, products, and students.
- Added case-insensitive search and field-based filtering.
- Generated record counts and numeric summaries (minimum, maximum, and average).
- Created a Flask web interface and a command-line tool.
- Added input validation and unit tests.
- Prepared the project for deployment on Render.

**Technologies:** Python, JSON, Flask, HTML/CSS, unittest, Git, GitHub, Render.

This project helped me strengthen my understanding of JSON handling, dictionaries and lists, data validation, testing, and deployment workflows.

GitHub: [PASTE YOUR REPOSITORY LINK]
Live demo: [PASTE YOUR RENDER LINK]

#Python #Flask #JSON #DataProcessing #GitHub #Render #LearningByBuilding

Only state that deployment/tests are complete after you have verified them. Replace the placeholders with your real links before posting.
