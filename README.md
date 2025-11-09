# Labs Project
This project consists of two parts:
* **Frontend (labs\_UI)** – built with **Angular 16.2.16** and **Node.js v18.19.0**
* **Backend (labs\_backend)** – built with **FastAPI** in Python

---

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```
Pull the latest changes anytime with:
```bash
git pull
```
---
### 2. Frontend (Angular)
Navigate to the `labs_UI` folder and install dependencies:
```bash
cd labs_UI
npm install
```
Start the Angular development server:
```bash
npm start
```
By default, the app runs at: [http://localhost:4200](http://localhost:4200)
---
### 3. Backend (FastAPI)
Navigate to the `labs_backend` folder and install dependencies:
```bash
cd labs_backend
pip install -r requirements.txt
```
Run the FastAPI server with:
```bash
uvicorn app.main:app --reload
```
The backend will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
---
## 📦 Tech Stack
* **Frontend:** Angular 16.2.16, Node.js v18.19.0
* **Backend:** FastAPI (Python 3.10+ recommended)
---
## 🛠 Notes
* Make sure **Node.js** and **Python** are installed.
* It’s recommended to use a **virtual environment** for Python dependencies:
```bash
python -m venv venv
source venv/bin/activate  # on Linux/Mac
venv\Scripts\activate     # on Windows
```
---
