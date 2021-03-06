#############################################################################
# Steve Iannaccone
# March 2017
#
# Flask app for running NCAA March Madness predictions
#############################################################################
from flask import Flask, request, url_for, render_template, request
import cPickle as pickle
import numpy as np
from datetime import datetime
from fuzzywuzzy import process

app = Flask(__name__)

# Form page to submit text
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def pnt_predicter():
    team1 = str(request.form['user_input1'])
    team2 = str(request.form['user_input2'])

    team1 = process.extractOne(team1, teamlist)[0]
    team2 = process.extractOne(team2, teamlist)[0]
    if (team1, team2) in predDict:
        spread = int(np.round(predDict[(team1, team2)]))
    elif (team2, team1) in predDict:
        spread = int(np.round(-1. * predDict[(team2, team1)]))
    else:
        spread = "Sorry! We can't find those teams..."


    team1_img = 'img/TeamLogos/{0}.png'.format(process.extractOne(team1,
                                                all_team_imgs)[0])

    team2_img = 'img/TeamLogos/{0}.png'.format(process.extractOne(team2,
                                                all_team_imgs)[0])

    now = datetime.now().date().month
    if now < 11 and now > 4:
        vegas_odds = [""]
        message = "Sorry, looks like we're between seasons. So you're money is safe...for now."
    else:
        message = "Might be time to call your Bookie...Go get 'em tiger!"


    return render_template('predict.html', team1=team1, team2=team2,
            point_spread=spread, team1_img=team1_img, team2_img=team2_img, vegas_odds=vegas_odds, message=message)



if __name__ == '__main__':
    all_team_imgs = pickle.load(open('data/all_team_imgs', 'rb'))
    teamlist = pickle.load(open('data/allTeamList2016', 'rb'))
    predDict = pickle.load(open('data/predDict2017', 'rb'))
    vegas_odds = pickle.load(open('data/vegas_odds', 'rb'))
    app.run(host='0.0.0.0', port=80, threaded=True)
