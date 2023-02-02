# You can identify fake source files by the file path in the title bar.
# Real: \Python\Python<version>\Lib\.

# first we import from flask the Flask class
from flask import Flask, render_template, request, redirect, send_file, after_this_request
from logic import process_pdf, exists, remove

# an object instance of this class is our WSGI application
# the __name__ variable is equal to the name of the module in which it is used
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', exists=exists('./uploads/CONVERTED-PDF.xlsx'))


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(f'uploads/{file.filename}')

    new_file_name = f'uploads/{file.filename}'

    process_pdf(new_file_name)

    remove(f'uploads/{file.filename[:-4]}.csv')
    remove(f'uploads/{file.filename[:-4]}.pdf')

    return redirect('/')


@app.route('/download')
def download():
    path = 'uploads/CONVERTED-PDF.xlsx'

    @after_this_request
    def remove_file(response):
        remove(path)
        print(response)
        return response

    return send_file(path, as_attachment=True, download_name='HERE-YA-GO.xlsx')


@app.route('/refresh')
def refresh():
    return redirect('/')
