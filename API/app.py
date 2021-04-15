from website.app import create_app
import pathlib
import os
from dotenv import load_dotenv
load_dotenv(f'{pathlib.Path(__file__).parent.absolute()}/.env')

app = create_app({
    'SECRET_KEY': 'secret',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'
})

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=5000, ssl_context=(os.environ['PATH_TO_CERT'], 
                                                                  os.environ['PATH_TO_KEY']))    