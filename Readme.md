# Travel Planner API 🌍

A RESTful API built with **FastAPI** for planning trips and collecting artworks (places to visit) from the **Art Institute of Chicago**.

## ✨ Features
- **Project Management:** Full CRUD for travel projects (Name, Description, Start Date).
- **Third-party Integration:** Real-time validation of places using the Art Institute of Chicago API.
- **Bulk Creation:** Create a project along with a list of places in a single request.
- **Business Logic:**
  - Limit: Maximum 10 places per project.
  - Unique Places: Prevents adding the same artwork to a project twice.
  - Auto-Completion: Projects are automatically marked as `is_completed` when all places are visited.
  - Data Protection: Projects cannot be deleted if they contain visited places.

## 🛠 Tech Stack
- **Framework:** FastAPI
- **Database:** SQLite (SQLAlchemy ORM)
- **Validation:** Pydantic
- **External API:** Requests

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/strixxjs/travel-planner>
  `cd travel_planner`

2. **Set up a VE:**
`python3 -m venv venv`
`source venv/bin/activate`

3. **Install dependencies:**
`pip install -r requirements.txt`

4. **Run the Server**
`uvicorn main:app --reload`


## **Once the server is running, the interactive Swagger documentation is available at:**

👉 http://localhost:8000/docs
