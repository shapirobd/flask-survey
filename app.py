from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisismysecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)


@app.route('/questions/<num>')
def question_page(num):
    if int(num) != len(responses):
        flash('You are trying to access an invalid question!', 'Error')
        return redirect(f'/questions/{len(responses)}')
    elif len(responses) == len(satisfaction_survey.questions):
        flash('You are trying to access an invalid question!', 'Error')
        return redirect('/thank-you')
    question = satisfaction_survey.questions[int(num)].question
    choices = satisfaction_survey.questions[int(num)].choices
    return render_template('question.html', question=question, choices=choices)


@app.route('/thank-you')
def thanks_page():
    return render_template('thanks.html')


@app.route('/answer', methods=['POST'])
def answer_page():
    responses.append(request.form['ans'])
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect('/thank-you')
