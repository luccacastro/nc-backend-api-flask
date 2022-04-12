from api import app
import os

if __name__ == "__main__":
    print(os.environ.get('PORT', 5000) +'---'*50)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=3000)