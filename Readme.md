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

## 📝 API Endpoints & Examples

### 1. Create a Project (Bulk Create)
**`POST /projects/`**

Creates a new travel project. You can include an array of `places` to validate and add them in the same request.

**Request Body:**
```json
{
  "name": "Art Tour in Paris",
  "description": "Weekend trip to see the masterpieces",
  "start_date": "2026-06-05",
  "places": [
    {
      "external_id": "27992",
      "notes": "Must see Tour Eiffel"
    }
  ]
} 
```

### 2. Mark a Place as Visited
**`PUT /projects/{project_id}/places/{place_id}/`**

Updates the notes or visited status of a specific place.

💡 Tip: If all places within a project are marked as `is_visited: true`, the project automatically updates to `is_completed: true`.

Request Body:
```json
{
  "notes": "Absolutely stunning in person!",
  "is_visited": true
}
```

### 3. Get Project Details
**`GET /projects/{project_id}`**

Retrieves full project details, including its completion status and a nested list of all saved artworks.

### 4. Update a Project
**`PUT /projects/{project_id}`**

Updates the basic information of a travel project.

**Request Body:**
```json
{
  "name": "Art Tour in Warszaw (Updated)",
  "description": "Extended trip for 5 days",
  "start_date": "2026-05-06"
}
```
### 5. Delete a Project
**`DELETE /projects/{project_id}`**

Removes a project and all its associated places from the database.

💡 Tip: This request will fail with a `400 Bad Request` if any place inside the project is already marked as `is_visited: true`.



## **Once the server is running, the interactive Swagger documentation is available at:**

👉 http://localhost:8000/docs
