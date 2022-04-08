from app.main import app
import sys
sys.path.insert(0, '/app')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
