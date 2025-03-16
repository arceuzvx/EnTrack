# EnTrack
An energy tracking web application that helps users monitor and reduce their energy consumption through task management and energy-saving tips.

## Features
- User authentication and profile management
- Task management system with AJAX functionality
  - Add, toggle, and delete tasks
  - Real-time updates without page refresh
- Daily energy-saving tips
- Modern, responsive UI with Tailwind CSS
- More features coming soon:
  - Track electricity and gas usage
  - Calculate energy savings
  - View historical energy consumption data
  - Compete on a leaderboard with other users

## Technologies Used
- Django 4.2.7
- Tailwind CSS
- jQuery (for AJAX functionality)
- Python-dotenv (for environment variables)

## Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arceuzvx/EnTrack.git
cd EnTrack
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=django-insecure-placeholder-key-for-development
```

5. Run migrations to set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser (admin account):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Access the application:
- Main application: http://127.0.0.1:8000/
- Admin interface: http://127.0.0.1:8000/admin/

## Usage
1. Register a new account or log in with existing credentials
2. Navigate to the dashboard to:
   - View and manage your tasks
   - See daily energy-saving tips
   - Track your progress
3. Use the task management system to:
   - Add new tasks by typing in the task input field
   - Mark tasks as complete by clicking the circle icon
   - Delete tasks using the trash icon
4. All task operations are performed in real-time using AJAX

## Troubleshooting
- If you encounter any issues with the database, try:
  ```bash
  python manage.py makemigrations dashboard
  python manage.py migrate
  ```
- Make sure all required environment variables are set in your `.env` file
- Check that you're using a compatible Python version
- Ensure all dependencies are installed correctly

## Contributors/Teammates
- Soumyshree Biswas [@soumyashb](https://github.com/soumyashb)
- Piyali Sarkar [@loopPXy](https://github.com/loopPXy)
- Sylvia Bhattacharjee [@8910sylvia](https://github.com/8910sylvia)
- Shreya Dutta [@arceuzvx](https://github.com/arceuzvx)

## License
This project is licensed under the MIT License.
