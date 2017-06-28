from flask import Flask,render_template,request,redirect
app_lulu = Flask(__name__)

app_lulu.vars={}

@app_lulu.route('/input_sentences',methods=['GET','POST'])
def index_lulu():
    if request.method == 'GET':
        return render_template('get_input_text.html')
    else:
        #request was a POST
        app_lulu.vars['input_text'] = request.form['input_text']

        f = open('%s.txt'%(app_lulu.vars['input_text']),'w')
        f.write(app_lulu.vars['input_text'])
        f.close()

        return render_template('show_output_layout.html',input_text = app_lulu.vars['input_text'], output = {'q1':'a1', 'q2': 'a2'})

@app_lulu.route('/next_page',methods=['POST'])
def next_lulu():
    return redirect('/input_sentences')
#
# @app_lulu.route('/usefulfunction_lulu',methods=['GET','POST'])
# def usefulfunction_lulu():
#     return render_template('layout_lulu.html',num=1,question='Which fruit do you like best?',ans1='banana',ans2='mango',ans3='pineapple')

if __name__ == "__main__":
    app_lulu.run(debug=True)
