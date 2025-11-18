

//ЗАПУСК//
source venv/bin/activate
# habittracker-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000