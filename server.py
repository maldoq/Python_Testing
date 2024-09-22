import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = next(
        (club for club in clubs if club['email']
         == request.form['email']), None,
    )
    print(club)
    if club is not None:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("this mail doesn't exists")
        return render_template('login.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash('Something went wrong-please try again')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [
        c for c in competitions if c['name']
        == request.form['competition']
    ][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired >= 1 and placesRequired <= 12:
        if int(club['points']) >= placesRequired:
            club['points'] = int(club['points'])-placesRequired
            if int(competition['numberOfPlaces']) >= placesRequired:
                competition['numberOfPlaces'] = int(
                    competition['numberOfPlaces'],
                )-placesRequired
                flash('Great-booking complete!')
            else:
                flash("The place ain't suficient or full. Sorry")
                return render_template('booking.html', club=club, competition=competition)
        else:
            flash(
                "Your points ain't suficient. You currently have: " +
                str(club['points']),
            )
            return render_template('booking.html', club=club, competition=competition)
    elif placesRequired == 0:
        flash('You must take at least 1 place')
        return render_template('booking.html', club=club, competition=competition)
    elif placesRequired < 0:
        flash('The value cannot be negative')
        return render_template('booking.html', club=club, competition=competition)
    else:
        flash('the value is bigger than 12, please reduce the value')
        return render_template('booking.html', club=club, competition=competition)
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
