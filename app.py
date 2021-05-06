from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "anystring"
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def get_homepage():
    """passes along the survey title and the instructions"""

    responses.clear()
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('start-page.html', title=title, instructions=instructions)


@app.route('/question/<int:question_index>')
def show_question(question_index):
    """passes along the survey question based on the index"""

    question = satisfaction_survey.questions[question_index]
    return render_template('question.html', question=question)


@app.route('/answer', methods=["POST"])
def get_answer():
    """records the selection and redirects to the next question or to the end"""

    selection = request.form['answer']
    responses.append(selection)
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/end')
    else:
        return redirect(f"/question/{len(responses)}")


@app.route('/end')
def go_to_end():
    """sends user to the end page"""

    responses = []
    return render_template('end.html')
