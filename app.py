from flask import Flask, render_template, redirect, request, url_for, flash 
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "ooogabooga"

# Store user responses here
responses = []

@app.route('/')
def home():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/questions/<int:question_id>')
def question(question_id):
    # Determine the current question index based on responses
    current_question_id = len(responses)

    # Redirect if the user tries to skip ahead or go to a nonexistent question
    if question_id != current_question_id:
        if question_id >= len(satisfaction_survey.questions):
            # Redirect to the thank you page if they try to access a non-existent question
            return redirect(url_for('thank_you'))
        else:
            flash("You're trying to access an invalid question. Redirecting to the correct question.")
            return redirect(url_for('question', question_id=current_question_id))

    # If the question_id is correct, render the question
    question = satisfaction_survey.questions[question_id]
    return render_template('questions.html', question=question, question_id=question_id)




@app.route('/answer', methods=['POST'])
def answer():
    # Get the answer from the form data
    answer = request.form['answer']
    responses.append(answer)

    # Determine the next question index
    next_question_id = len(responses)

    # Redirect to the next question or the "Thank You" page
    if next_question_id < len(satisfaction_survey.questions):
        return redirect(url_for('question', question_id=next_question_id))
    else:
        return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/reset')
def reset():
    responses.clear()
    return redirect(url_for('home'))
