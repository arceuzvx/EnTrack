# EnTrack
An energy tracking web application that helps users monitor and reduce their energy consumption.

## Features
- Track electricity and gas usage
- Calculate energy savings
- View historical energy consumption data
- Compete on a leaderboard with other users
- Get energy-saving tips
- Manage energy-saving tasks

## Technologies Used
- Django 4.2.7
- Bootstrap 4
- Crispy Forms
- Chart.js (for data visualization)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/EnTrack.git
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
SECRET_KEY=your-secret-key
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Access the application at http://127.0.0.1:8000/

## Usage
1. Register a new account or log in with existing credentials
2. Navigate to the dashboard to view your energy consumption
3. Use the calculator to estimate your energy usage and savings
4. Track your progress in the history section
5. Compete with others on the leaderboard

## Contributors/Teammates
- Soumyshree Biswas [@soumyashb](https://github.com/soumyashb)
- Piyali Sarkar [@loopPXy](https://github.com/loopPXy)
- Sylvia Bhattacharjee [@8910sylvia](https://github.com/8910sylvia)
- Shreya Dutta [@arceuzvx](https://github.com/arceuzvx)
