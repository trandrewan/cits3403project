#Storing the routes for the website
#Anything thats not authenticatio nrelated that the user can naviagte to

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import openai

views = Blueprint("views", __name__)

openai.api_key = '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'

@views.route('/')
@login_required   #cannot access the homepage unless you are logged in
def home():
    return render_template("home.html",user=current_user)   #We will now be able to reference the current user and check if its logged in. If it is lgoged in, we can access all the imformatiomn about it


@views.route("/api", methods=["POST"])
@views.route("/api", methods=["POST"])
def api():
    message = request.json.get("message")
    username = request.json.get("username")

    # Define a list of cricket-related keywords
    cricket_keywords = ['cricket', 'bat', 'ball', 'wicket', 'pitch', 'stumps', 'run', 'batsman', 'bowler', 'all-rounder',
    'captain', 'umpire', 'fielder', 'catch', 'bowl', 'batting', 'bowling', 'fielding', 'innings', 'over',
    'test match', 'one-day international', 'odi', 'twenty20', 't20', 'toss', 'duck', 'century', 'fifty',
    'boundary', 'six', 'yorker', 'spin', 'fast bowling', 'lbw', 'leg before wicket', 'stumped', 'run-out',
    'appeal', 'drs', 'decision review system', 'maiden over', 'powerplay', 'power hitter', 'helmet',
    'gloves', 'pads', 'boundary rope', 'silly point', 'slip', 'cover drive', 'reverse swing', 'cricket bat grip',
    'fielding positions', 'batting average', 'bowling average', 'runs', 'wickets', 'innings', 'matches played',
    'centuries', 'half-centuries', 'fours', 'sixes', 'strike rate', 'economy rate', 'best bowling figures',
    'highest individual score', 'total runs scored', 'total wickets taken', 'batting strike rate',
    'bowling strike rate', 'batting partnerships', 'catches', 'run-outs', 'dismissals', 'maiden overs',
    'dot balls', 'overs bowled', 'bowling variations', 'number of matches won', 'number of matches lost',
    'number of matches drawn', 'win percentage', 'loss percentage', 'dot ball percentage',
    'batting average against specific opposition', 'bowling average against specific opposition', 'team rankings',
    'player rankings', 'player of the match', 'player of the series', 'hat-trick', 'duck percentage',
    'run rate', 'average run rate', 'average balls per wicket', 'boundary percentage',
    'dot ball percentage in powerplay', 'catches per match', 'stumping percentage', 'partnership records',
    'run chase success rate', 'most valuable player', 'mvp', 'batting records', 'bowling records',
    'highest team score', 'lowest team score', 'fastest century', 'fastest fifty', 'most runs in a series',
    'most wickets in a series', 'most sixes in a career', 'most fours in a career', 'most centuries in a career',
    'most five-wicket hauls in a career', 'most catches by a fielder', 'most stumpings by a wicketkeeper',
    'most dismissals by a wicketkeeper', 'best batting average in a career', 'best bowling average in a career',
    'best economy rate in a career', 'most matches as captain', 'most runs as captain', 'most wickets as captain',
    'most catches as captain', 'most sixes in an innings', 'most fours in an innings', 'most wickets in an innings',
    'most runs in a calendar year', 'most wickets in a calendar year', 'most centuries in a calendar year',
    'most dismissals in a calendar year', 'highest individual score in a match', 'best bowling figures in a match',
    'fastest ball bowled', 'most matches played by a player', 'most consecutive matches played']


    # Convert the user's message to lowercase and split it into words
    words = message.lower().split()

    # If none of the words in the user's message are in the list of cricket keywords, return an error message
    if not any(word in cricket_keywords for word in words):
        return jsonify({"message": "I'm sorry, I can only answer cricket-related questions."})

    # Otherwise, process the message as before
    # ...

    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    if completion.choices[0].message['content'] is not None:
        return jsonify({"message": completion.choices[0].message['content']})

    else :
        return 'Failed to Generate response!'