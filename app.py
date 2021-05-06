from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "anystring"
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
"""starting page route"""

# When homepage url is entered this view function passes along the survey title and instructions


def get_homepage():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('start-page.html', title=title, instructions=instructions)


@app.route('/question/<int:question_index>')
"""question page route based on the question index"""

# This function passes along a survey question based on the index


def show_question(question_index):
    question = satisfaction_survey.questions[question_index]
    return render_template('question.html', question=question)


@app.route('/answer', methods=["POST"])
"""This route receives the selection made for each question"""

# This function records the selection and redirects to either the next question or the end


def get_answer():
    selection = request.form['answer']
    responses.append(selection)
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/finished')
    else:
        return redirect(f"/question/{len(responses)}")
