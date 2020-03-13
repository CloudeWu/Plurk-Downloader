# -*- coding:utf-8 -*
# import packages
from flask import Flask, render_template, request, jsonify, Response
import json
import traceback
import functions.crawl as function

import home  # home page rendering 
    
##################
#                #
#   API server   #
#                #
##################
app = Flask(__name__)

# upload json { "link": "plurk url" } to get clear data
@app.route('/backup',methods=['GET','POST'])
def upload_file():
    if request.method == 'GET':
        return "please choose post method"

    if request.method == 'POST':
        try:
            url = request.json.get('link')
            print('Receive link\n', url)
            raw_data = function.get_content_by_link(url)
            # print(raw_data)
        except Exception as e:
            print("ERROR", {'error': str(e), 'trace': traceback.format_exc()})
            msg = {
                "status":"fail", 
                "reason":"500 Server Internal Error"
            }
            return jsonify(msg)

        return jsonify(raw_data)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response

if __name__ == '__main__':
    # register blueprints
    app.register_blueprint(home.bp)
    
    app.run(host='0.0.0.0', port=8765, debug=True)
    

