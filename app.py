from flask import Flask, render_template, request
from prediction_service.prediction import get_response
import os

webapp_root = 'webapp'

static_dir =  os.path.join(webapp_root, 'static')
template_dir  = os.path.join(webapp_root, 'templates')

app =  Flask(__name__, static_folder=static_dir, template_folder=template_dir)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        result = get_response(url)
        return render_template('response2.html', result_message = result['message'],
                               gif_link = result['gif_link'],
                               general_analysis_report = result['general_analysis_report'],
                               phish_prob = result['phis_prob'],
                               legal_prob = result['legal_prob'])
    return render_template('index.html')

# @app.route('/response')
# def response():
#     result = request.args.get('result')
#     return render_template('response.html', result=result)

# def process_url(url):
#     # Process the URL and retrieve the necessary information
#     # This is just a placeholder function, you should implement your own logic here
#     return {
#         'field1': 'Value 1',
#         'field2': 'Value 2',
#         'field3': 'Value 3',
#         'field4': 'Value 4'
#     }

if __name__ == '__main__':
    app.run(debug=True)
