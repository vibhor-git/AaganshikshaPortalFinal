
from app import app

if __name__ == '__main__':
    # Using the same port as defined in app.py for consistency
    app.run(host='0.0.0.0', port=5001, debug=True)
