from app import app, db
from app.models import User, Post
# Running shell command allows you to import processes without having to manually import them every time
@app.shell_context_processor # registers function as a shell context function; invoked when flask shell command runs
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post} # dictionary returned because for each item you must also provide a name under which it will be refrenced in the shell, here given by the dictionary keys