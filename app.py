from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "anystring"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'


@app.route('/')
def get_homepage():
    """passes along the survey title and the instructions"""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('start-page.html', title=title, instructions=instructions)


@app.route('/reset-responses', methods=['POST'])
def set_responses():
    """need to add some comments"""

    session[RESPONSES_KEY] = []
    return redirect('/question/0')


@app.route('/question/<int:question_index>')
def show_question(question_index):
    """passes along the survey question based on the index"""

    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')

    if (len(satisfaction_survey.questions) == len(responses)):
        return redirect('/end')

    if question_index != len(responses):
        flash(
            "You are trying to acces an invalid question. Please answer the question below.")
        return redirect(f"/question/{len(responses)}")

    question = satisfaction_survey.questions[question_index]
    return render_template('question.html', question=question)


@app.route('/answer', methods=["POST"])
def get_answer():
    """records the selection and redirects to the next question or to the end"""

    selection = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(selection)
    session[RESPONSES_KEY] = responses
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/end')
    else:
        return redirect(f"/question/{len(responses)}")


@app.route('/end')
def go_to_end():
    """sends user to the end page"""

    responses = []
    return render_template('end.html')
