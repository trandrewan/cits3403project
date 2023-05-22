#Storing the routes for the website
#Anything thats not authenticatio nrelated that the user can naviagte to

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from . import db
import openai
import os
from dotenv import load_dotenv
views = Blueprint("views", __name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    'test match', 'one day', 'odi','50', 'twenty20', 't20','twenty', 'toss', 'duck', 'century', 'fifty',
    'boundary', 'six', 'four', 'yorker', 'spin', 'batter', 'bowler,' 'lbw', 'leg before wicket', 'stumped', 'run-out',
    'appeal', 'drs', 'decision review system', 'maiden', 'powerplay', 'power hitter', 'helmet',
    'gloves', 'pads', 'boundary', 'silly point', 'slip', 'cover drive', 'reverse', 'swing', 'grip', 'fielding', 'average', 'runs', 'wickets', 'innings', 'matches',
    'centuries', 'half-centuries', 'fours', 'sixes', 'rate', 'figures',
    'score', 'scored', 'total wickets taken', 'partnerships', 'catches', 'run outs', 'dismissals', 'maiden', 'maidens'
    'dot','dots', 'overs', 'variations', 'won', 'lost',
    'drawn', 'percentage', 'percentage', 'dot-ball',
    'rankings', 'player rankings', 'player of the match', 'player of the series', 'hat-trick', 'duck percentage',
    'run rate', 'average run rate', 'average balls per wicket', 'boundary percentage', 
    'catches per match', 'stumping percentage', 'partnership records',
    'run chase success rate', 'most valuable player', 'mvp', 'records', 'bowling records',
    'highest', 'lowest', 'fastest century', 'fastest fifty', 'most runs in a series',
    'most wickets in a series', 'most sixes in a career', 'most fours in a career', 'most centuries in a career',
    'most five-wicket hauls in a career', 'most catches by a fielder', 'most stumpings by a wicketkeeper',
    'most dismissals by a wicketkeeper', 'career', 'best bowling average in a career',
    'best economy rate in a career', 'most matches as captain', 'most runs as captain', 'most wickets as captain',
    'most catches as captain', 'most sixes in an innings', 'most fours in an innings', 'most wickets in an innings',
    'most runs in a calendar year', 'most wickets in a calendar year', 'most centuries in a calendar year',
    'most dismissals in a calendar year', 'best bowling figures in a match',
    'fastest ball bowled', 'most matches played by a player', 'most consecutive matches played',"wicket", "run", 
    "boundary", "over", "innings", "bowler", "batsman", "fielder", "umpire", "captain", "pitch", "stumps", "crease", 
    "lbw", "yorker", "bouncer", "spinner", "seamer", "off-spinner", "leg-spinner", "googly", "reverse swing", 
    "cover drive", "square cut", "pull shot", "hook shot", "sweep shot", "yorker", "doosra", "slog sweep", "slip", 
    "gully", "silly point", "long on", "long off", "mid-wicket", "fine leg", "deep square leg", "deep mid-wicket", 
    "deep cover", "deep point", "deep fine leg", "powerplay", "wide", "no-ball", "six", "four", "catch",
    "stumping", "run out", "follow-on", "toss", "toss winner", "fielding", "batting", "bowling", "all-rounder",
    "maiden over", "century", "fifty", "double century", "triple century", "hat-trick", "drs", "run rate",
    "economy rate", "strike rate", "maiden", "extra", "appeal", "review", "power hitter", "pinch hitter",
    "nightwatchman", "day-night match", "toss", "on-drive", "leg glance", "inside edge", "outside edge", 
    "leg before wicket", "fielding restrictions", "sweep", "block", "drive", "flick", "run chase", "declaration", 
    "retire hurt", "lbw review", "caught behind", "helmet", "gloves", "pads", "ball", "bails", "boundary rope", 
    "boundary fielder", "boundary line", "run-up", "follow-through", "run-up", "in-swinger", "out-swinger", 
    "full toss", "half-volley", "short delivery", "run-up", "dead ball", "fielding circle", "fine leg", "silly mid-on",
    "silly mid-off", "mid-on", "mid-off", "mid-wicket", "extra cover", "deep point", "deep square leg", "deep mid-wicket",
    "third man", "long leg", "long-off", "long-on", "cover", "cover point", "short leg", "deep backward square leg", 
    "short third man", "backward point", "backward square leg", "fine leg", "cow corner", "deep mid-wicket", "long leg", 
    "straight drive", "leg break", "off break", "arm ball", "flipper", "googly", "carrom ball", "top edge", "leading edge", 
    "middle stump", "off stump", "leg stump", "no-ball", "free hit", "wide", "dead ball", "bye", "leg bye", "toss", "ground", 
    "slip fielder", "gully fielder", "short leg fielder", "square leg fielder", "mid-on fielder", "mid-off fielder", 
    "mid-wicket fielder", "long-on fielder", "long-off fielder", "cover fielder", "point fielder", "fine leg fielder", 
    "third man fielder", "deep square leg fielder", "backward point fielder", "extra cover fielder", "deep mid-wicket fielder", 
    "run rate", "economy rate", "boundary count", "dls method", "rain delay", "boundary fielding", "circle", "boundary fielding", 
    "outside edge", "inside edge", "switch hit", "helicopter shot", "paddle sweep", "reverse sweep", "dilscoop", "knuckleball", 
    "toe-crusher", "yorker", "slower ball", "leg glance", "helicopter shot", "top edge", "leading edge", "clean bowled", 
    "caught and bowled", "hit-wicket", "leg before wicket", "run out", "stump", "stumped", "strike", "non-striker", "tailender", 
    "fielding coach", "batting coach", "bowling coach", "match referee", "third umpire", "square leg umpire", "leg umpire", 
    "on-field umpire", "reserve umpire", "off side", "leg side", "follow-on", "square leg", "mid-wicket", "deep mid-wicket", 
    "third man", "backward point", "fine leg", "leg break", "off break", "inswinger", "outswinger", "googly", "chinaman", 
    "flipper", "arm ball", "yorker", "bouncer", "slower ball", "full toss", "half-volley", "wickets", "runs", "boundaries", 
    "overs", "innings", "bowlers", "batsmen", "fielders", "umpires", "captains", "pitches", "stumps", "creases", "lbws", 
    "yorkers", "bouncers", "spinners", "seamers", "off-spinners", "leg-spinners", "googlies", "reverse swings", 
    "cover drives", "square cuts", "pull shots", "hook shots", "sweep shots", "yorkers", "doosras", "slog sweeps", 
    "slips", "gullies", "silly points", "long ons", "long offs", "mid-wickets", "fine legs", "deep square legs", 
    "deep mid-wickets", "deep covers", "deep points", "deep fine legs", "powerplays", "wides", 
    "no-balls", "sixes", "fours", "catches", "stumpings", "run outs", "follow-ons", "tosses", "toss winners", "fieldings", 
    "battings", "bowlings", "all-rounders", "maiden overs", "centuries", "fifties", "double centuries", "triple centuries", 
    "hat-tricks", "drs", "run rates", "economy rates", "strike rates", "maidens", "extras", "appeals", "reviews", "power hitters",
    "pinch hitters", "nightwatchmen", "day-night matches", "tosses", "on-drives", "leg glances", "inside edges", "outside edges",
    "leg before wickets", "fielding restrictions", "sweeps", "blocks", "drives", "flicks", "run chases", "declarations", 
    "retire hurts", "lbw reviews", "caught behinds", "helmets", "gloves", "pads", "balls", "bails", "boundary ropes", 
    "boundary fielders", "boundary lines", "run-ups", "follow-throughs", "run-ups", "in-swingers", "out-swingers", "full tosses", 
    "half-volleys", "short deliveries", "run-ups", "dead balls", "fielding circles", "fine legs", "silly mid-ons", "silly mid-offs",
    "mid-ons", "mid-offs", "mid-wickets", "extra covers", "deep points", "deep square legs", "deep mid-wickets", "third men",
    "long legs", "long-offs", "long-ons", "covers", "cover points", "short legs", "deep backward square legs", "short third men", 
    "backward points", "backward square legs", "fine legs", "cow corners", "deep mid-wickets", "long legs", "straight drives", 
    "leg breaks", "off breaks", "arm balls", "flippers", "googlies", "carrom balls", "top edges", "leading edges", "middle stumps", 
    "off stumps", "leg stumps", "no-balls", "free hits", "wides", "dead balls", "byes", "leg byes", "tosses", "grounds", 
    "slip fielders", "gully fielders", "short leg fielders", "square leg fielders", "mid-on fielders", "mid-off fielders", 
    "mid-wicket fielders", "long-on fielders", "long-off fielders", "cover fielders", "point fielders", "fine leg fielders", 
    "third man fielders", "deep square leg fielders", "backward point fielders", "extra cover fielders", 
    "deep mid-wicket fielders", "run rates", "economy rates", "boundary counts", "dls methods", "rain delays", 
    "boundary fieldings", "circles", "boundary fieldings", "outside edges", "inside edges", "switch hits", 
    "helicopter shots", "paddle sweeps", "reverse sweeps", "dilscoops", "knuckleballs", "toe-crushers", 
    "yorkers", "slower balls", "leg glances", "helicopter shots", "top edges", "leading edges", "clean bowleds", 
    "caught and bowleds", "hit-wickets", "leg before wickets", "run outs", "stumps", "stumpeds", "strikes", 
    "non-strikers", "tailenders", "fielding coaches", "batting coaches", "bowling coaches", "match referees", 
    "third umpires", "square leg umpires", "leg umpires", "on-field umpires", "reserve umpires", "off sides", "leg sides",
    "follow-ons", "square legs", "mid-wickets", "deep mid-wickets", "third men", "backward points", "fine legs", "leg breaks",
    "off breaks", "ins", "afghanistan", "australia", "bangladesh", "bermuda", "canada", "england", "hong kong", "india",
    "ireland", "kenya", "namibia", "netherlands", "new zealand", "oman", "pakistan", "papua new guinea", "scotland",
    "south africa", "sri lanka", "united arab emirates", "united states", "west indies", "zimbabwe", "bradman", "tendulkar", 
    "ponting", "lara", "richards", "sobers", "warne", "kallis", "akram", "akhtar", "hadlee", "pollock", "waugh", "waqar", "miandad", 
    "gavaskar", "lloyd", "kapil", "dravid", "hayden", "sanga", "muralitharan", "steyn", "s smith", "kohli", "gibbs", "sehwag", 
    "gilchrist", "ambrose", "border", "boycott", "hoggard", "sarwan", "jayasuriya", "ganguly", "laxman", "klusener", "vaughan", 
    "hughes", "hussey", "chanderpaul", "s waugh", "jones", "flintoff", "sachin", "afridi", "holding", "morkel", "perera", "sanga", 
    "lara", "sangakkara", "kumble", "laxman", "kapil", "sobers", "ponting", "waugh", "hussey", "akram", "ambrose", "lloyd", 
    "hadlee", "steyn", "kallis", "gavaskar", "dravid", "hayden", "sehwag", "smith", "warne", "mcgrath", "pollock", "akhtar", 
    "miandad", "klusener", "gilchrist", "sarwan", "jayasuriya", "muralitharan", "border", "vaughan", "ganguly", "chanderpaul", 
    "hughes", "hoggard", "vaas", "hussey", "jones", "flintoff", "afridi", "taylor", "anderson", "mcgrath", "taylor", 
    "jayawardene", "langer", "sharma", "azharuddin", "siddique", "simmons", "raza", "hafeez", "inzamam", "malik", "trott", 
    "stokes", "collingwood", "mccullum", "dhoni", "yuvraj", "shastri", "gambhir", "younis", "fleming", "imran", "border", 
    "willis", "herath", "kumble", "amir", "saeed", "sehwag", "hayden", "gambhir", "wasim", "waqar", "anderson", "stokes", 
    "collingwood", "shastri", "saeed", "raza", "herath", "malik", "trott", "azharuddin", "amir", "siddique", "fleming", 
    "imran", "mccullum", "yuvraj", "dhoni", "sharma", "langer", "willis", "inzamam", "hafeez", "gambhir", "rahane", "vettori", 
    "rahane", "vettori", "sarfraz", "anderson", "morris", "jadeja", "anderson", "morris", "jadeja", "cairns", "utherford", 
    "giles", "herath", "pathan", "jayawardene", "crowe", "dravid", "taylor", "badrinath", "cairns", "utherford", "giles", "pathan", 
    "crowe", "badrinath", "yadav", "williamson", "voges", "waugh", "gilchrist", "younis", "harmison", "yadav", "williamson", 
    "voges", "harmison", "gayle", "ganguly", "symonds", "symonds", "afridi", "gayle", "ganguly", "zaheer", "vaas", "jayawardene", 
    "sachin", "lara", "waugh", "morkel", "moody", "langer", "lara", "sachin", "moody", "zaheer", "morkel", "waugh", "jayawardene", 
    "country", "countries", "players", "batsmen", "cricketers", "ball", "bat", "fielder", "lords", "oval", "melbourne", "sydney", 
    "eden gardens", "mumbai", "adelaide", "perth", "cape town", "centurion", "durban", "chennai", "bangalore", "karachi", "lahore", 
    "rawalpindi", "multan", "kolkata", "ahmedabad", "colombo", "galle", "pallekele", "dubai", "sharjah", "abu dhabi", "trent bridge", 
    "old trafford", "headingley", "the gabba", "waca", "port of spain", "barbados", "kingston", "antigua", "georgetown", "guyana", 
    "chittagong", "dhaka", "hamilton", "wellington", "christchurch", "auckland", "dunedin", "brisbane", "adelaide oval", "perth stadium", 
    "sydney cricket ground", "melbourne cricket ground", "eden park", "the oval", "newlands", "st george's park", "wanderers stadium", 
    "super sport park", "hagley oval", "bay oval", "sheikh zayed stadium", "r premadasa stadium", "sardar patel stadium", "motera stadium", 
    "sindh cricket association stadium", "rajiv gandhi international cricket stadium", "arun jaitley stadium", "feroz shah kotla", 
    "wankhede stadium", "the village", "the keenan stadium", "arunachal pradesh cricket association stadium", "barabati stadium", 
    "andhra cricket association-vdca cricket stadium", "vidarbha cricket association stadium", "m chinnaswamy stadium", "brabourne stadium", 
    "srikantadatta narasimha raja wadiyar ground", "rajiv gandhi international stadium", "jawaharlal nehru stadium", "green park", 
    "udaipur cricket ground", "malahide cricket club ground", "castle avenue", "civil service cricket club", "eglinton cricket club", 
    "oak hill cricket club", "the hague", "rotterdam", "hazelaarweg", "bermuda national stadium", "somerset cricket club", "warner park cricket stadium", 
    "queen's park oval", "brian lara stadium", "kensington oval", "sabina park", "arnos vale stadium", "providence stadium", 
    "demerara cricket club ground", "queen's park cricket club", "spartan cricket club ground", "sir vivian richards stadium", 
    "sri lankas ports authority cricket club ground", "sinhalese sports club ground", "r premadasa stadium", 
    "rajiv gandhi international stadium", "tribhuvan university international cricket ground", "bay oval", "mcg", "marrara cricket ground",
    "traeger park", "city oval", "amy's square", "kaliningrad stadium", "lowest", "best", "average", "averages", "test", "one day international",
    "odi", "t20 international", "first class", "list a", "twenty20", "domestic t20 league", "ipl", "most", "least", "technique", "play", "cricket",
    "international", "stadiums", "stadium", "ground", "pitch", "statistics", "stats", "women", "women's", "womens", "team", "teams", "home", "away","ashes","hello","hi","how are you",
    "thanks", "thank you", 'bye','goodbye','morning','afternoon']


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