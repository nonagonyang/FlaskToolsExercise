# Step Two: The Start Page
# initialize a variable called responses to be an empty list
# keep track of the user’s survey responses with this list
# As people answer questions, their answers get stored in this list.

responses=[]

# make a server with flask
from flask import Flask,render_template,request,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
app= Flask(__name__)
app.config['SECRET_KEY'] = 'surveykeykey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

from surveys import satisfaction_survey


# handle first request
# render a page that shows the user the title of the survey
# the instructions, and a button to start the survey
# The button should serve as a link that directs the user to /questions/0 
# (the next step will define that route).
@app.route("/")
def show_survey():
    survey_title=satisfaction_survey.title
    survey_instruction=satisfaction_survey.instructions
    return render_template("home.html",survey_title=survey_title,survey_instruction=survey_instruction)

@app.route("/begin", methods=["POST"])
def start_survey():
    return redirect("/questions/0")


# Step Three: The Question Page
# build a route that can handle questions 
# it should handle URLs like /questions/0 (the first question), 
# /questions/1, and so on.
# When the user arrives at one of these pages, 
# it should show a form asking the current question, 
# and listing the choices as radio buttons. 
@app.route("/questions/<int:questionid>")
def show_question(questionid):
    if (len(responses) != questionid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {questionid}.")
        return redirect(f"/questions/{len(responses)}")
    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions, redirect them to thank you page
        return redirect("/thankyou")
    question = satisfaction_survey.questions[questionid]
    return render_template("questions.html", question=question,)

# Step Four: Handling Answers
# When the user submits an answer, 
# you should append this answer to your responses list, 
# and then redirect them to the next question.

@app.route("/answer", methods=["POST"])
def handle_answer():
    answer=request.form["answer"]
    responses.append(answer)
    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/thankyou")

    else:
        return redirect(f"/questions/{len(responses)}")


# Step Five: Thank The User
# The customer satisfaction survey only has 4 questions, 
# so once the user has submitted four responses, 
# there is no new question to task. Once the user has answered all questions, 
# rather than trying to send them to /questions/5, 
# redirect them to a simple “Thank You!” page.

@app.route("/thankyou")
def thank_user():
    return render_template("thankyou.html")


