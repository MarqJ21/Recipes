from flask_app.controllers import user_controller
from flask_app.controllers import recipe_controller
from flask_app import app

if __name__=='__main__':
    app.run(debug=True, port = 5001)