from flask import Flask
import subprocess
app = Flask(__name__)

@app.route('/')
def hello_world():
    cmd = "echo 'sudo systemctl restart dl' | at now + 1 minutes"
    return subprocess.check_output([
       "bash", "-c", cmd])

if __name__ == '__main__':
    app.run( host='0.0.0.0')
