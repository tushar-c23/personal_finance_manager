# Personal Finance Manager
Backend system for a personal finance management system with the following features:
- User registration and login
- User can add, edit, delete, and view transactions
- Categorised transactions
- Users can create custom categories
- Users can make savings goals and the system will track their progress based on categories associated with the goals
- Users can view their spending habits in a graphical format
- Users can generate monthly and yearly reports
- Users can generate monthly and yearly reports based on categories

## Technologies
- FastAPI
- SQLAlchemy for ORM
- SQLite as the database (`test.db` is the database file, pushed to the repo for easy testing)
- Pydantic
- Matplotlib

## Directory Structure
```
personal_finance_manager
│   README.md
│   main.py
│   requirements.txt
│   test.db
│   .gitignore
│   models.py
│   schemas.py
|   database.py
|   __init__.py
│---controllers
│   │   __init__.py
│   │   auth_controller.py
│   │   category_controller.py
│   │   report_controller.py
│   │   transaction_controller.py
│   │   user_controller.py
|   |   saving_goal_controller.py
│---services
│   │   __init__.py
│   │   auth_service.py
|   |   category_service.py
|   |   report_service.py
|   |   transaction_service.py
|   |   user_service.py
|   |   saving_goal_service.py
|---routes
|   |   __init__.py
|   |   auth.py
|   |   category.py
|   |   report.py
|   |   transaction.py
|   |   user.py
|   |   saving_goal.py
```
The code is structured in a way that follows the MVC pattern.
- The `controllers` directory contains the controllers for each entity which handle business logic.
- The `services` directory contains the services for each entity which handle the pipeline with the database.
- The `routes` directory contains the routes for each entity which generate the api routes for each module.

The code itself is really verbose with self-explanatory variable names. The code is also well documented.

## How to
### Clone the repository
```bash
git clone https://github.com/tushar-c23/personal_finance_manager.git
```

### Install dependencies
Navigate to the project directory and run the following command:
```bash
pip install -r requirements.txt
```

### Run the dev server
Navigate to the project directory and run the following command:
```bash
fastapi dev main.py
```

### API Documentation
Navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation.

### Postman Collection
You can download the postman collection and environment from [here](https://drive.google.com/drive/folders/1ZT8ZDlgmEK-yNRpJVz9_ftFpb_hjc4va?usp=sharing)

**Instructions:**
1. Import the json collections and the environment in postman to get readymade API requests with tests
2. Signup as a user (optional)
3. Login as a user (you can use pre filled user in the db)<br>
	These are the credentials:<br>
	username: `tushar` <br>
	password: `test`
4. After login change the `access_token` variable in the "**Syfe**" environment to the "**access_token**" value received in the response of login api call.
5. Use all the APIs as required

## Notes
- The pie charts returned in the reports are in Base64 encoded format. You can decode them using any [online tool](https://base64.guru/converter/decode/image) to view the image.