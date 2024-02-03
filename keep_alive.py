from flask import Flask, render_template, redirect
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/display_txt')

@app.route('/display_txt')
def display_txt():
    # Change 'your_text_file.txt' to the actual path of your text file
    file_path = 'logger.txt'

    with open(file_path, 'r') as file:
        lines = file.readlines()

    return render_template('index.html', lines=lines)

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    keep_alive()
