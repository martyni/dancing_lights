from flask import Flask
import subprocess
app = Flask(__name__)

@app.route('/')
def restarr():
    cmd = "echo 'sudo systemctl restart dl' | at now + 1 minutes"
    page = '<pre style="font-size: 45px"> {} </pre>'
    return page.format(
            subprocess.check_output([
        "bash", "-c", cmd],
        stderr=subprocess.STDOUT
        ).decode("utf-8")
    )



@app.route('/status')
def status():
    return subprocess.check_output([
       "systemctl", "status", "dl"])



if __name__ == '__main__':
    app.run( host='0.0.0.0')
