from flask import Flask, render_template, redirect, request, url_for, flash, session
from surveys import satisfaction_survey, personality_quiz
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "ooogabooga"

# Store user responses here
responses = []

@app.route('/')
def home():
    return render_template('start.html')

@app.route('/surveys')
def surveys_page():
    return render_template('surveys.html', surveys=surveys)

@app.route('/start/<survey_code>', methods=['POST'])
def start_survey(survey_code):
    session["responses"] = []  # Initialize responses in session
    return redirect(url_for('question', question_id=0, survey_code=survey_code))

@app.route('/questions/<int:question_id>/<survey_code>')
def question(question_id, survey_code):
    current_question_id = len(session.get("responses", []))

    if question_id != current_question_id:
        if question_id >= len(surveys[survey_code].questions):
            return redirect(url_for('thank_you'))
        else:
            flash("You're trying to access an invalid question. Redirecting to the correct question.")
            return redirect(url_for('question', question_id=current_question_id, survey_code=survey_code))

    question = surveys[survey_code].questions[question_id]
    return render_template('questions.html', question=question, question_id=question_id, survey_code=survey_code)  # Make sure survey_code is included



@app.route('/answer/<survey_code>', methods=['POST'])
def answer(survey_code):
    answer = request.form['answer']
    responses = session.get("responses", [])
    responses.append(answer)
    session["responses"] = responses  # Save updated responses back to session

    # Determine the next question index
    next_question_id = len(responses)

    if next_question_id < len(surveys[survey_code].questions):
        return redirect(url_for('question', question_id=next_question_id, survey_code=survey_code))
    else:
        return redirect(url_for('thank_you'))




@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/reset', methods=['POST'])
def reset_survey():
    session.pop("responses", None)  # Clear the responses from the session
    return redirect(url_for('home'))

