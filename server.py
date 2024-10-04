import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
    return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
    return listOfCompetitions


def save_data_to_file(data, filename):
    """Save the updated data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


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


def filter_upcoming_competitions(competitions):
    """Return a list of competitions that are upcoming."""
    current_datetime = datetime.now()
    return [comp for comp in competitions if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > current_datetime]


@app.route('/showSummary', methods=['POST'])
def showSummary():
    upcoming_competitions = filter_upcoming_competitions(competitions)
    club = next(
        (club for club in clubs if club['email'] == request.form['email']),
        None,
    )
    if club:
        return render_template('welcome.html', club=club, competitions=upcoming_competitions)
    else:
        flash("This email doesn't exist")
        return render_template('login.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = next(c for c in clubs if c['name'] == club)
        foundCompetition = next(c for c in competitions if c['name'] == competition)
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    except StopIteration:
        flash('Club or competition not found. Please try again.')
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        upcoming_competitions = filter_upcoming_competitions(competitions)
        competition_name = request.form.get('competition')
        club_name = request.form.get('club')
        places_required = request.form.get('places')

        if not competition_name or not club_name or not places_required:
            flash('Missing required form data. Please try again.')
            return redirect(url_for('login'))

        placesRequired = int(places_required)

        competition = next(c for c in competitions if c['name'] == competition_name)
        club = next(c for c in clubs if c['name'] == club_name)

        # Get the current number of bookings for the club in this competition
        already_booked = competition['bookings'].get(club_name, 0)

        # Calculate the total places after the new booking
        total_booked = already_booked + placesRequired

        # Ensure the total does not exceed 12
        if total_booked > 12:
            flash(
                f'You can only book a maximum of 12 places per competition. You have already booked {already_booked} places.'
            )
            return render_template('booking.html', club=club, competition=competition)

        if 1 <= placesRequired <= 12:
            if int(club['points']) >= placesRequired:
                if int(competition['numberOfPlaces']) >= placesRequired:
                    # Update the competition and club data
                    club['points'] = int(club['points']) - placesRequired
                    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired

                    # Update the club's bookings
                    competition['bookings'][club_name] = total_booked

                    flash('Great - booking complete!')

                    # Save changes to the files
                    # save_data_to_file({'clubs': clubs}, 'clubs.json')
                    # save_data_to_file({'competitions': competitions}, 'competitions.json')

                    # Redirect to welcome.html after booking
                    return render_template('welcome.html', club=club, competitions=upcoming_competitions)
                else:
                    flash('Not enough places available. Please try again.')
            else:
                flash(f'Insufficient points. You currently have: {club["points"]}')
        else:
            if placesRequired == 0:
                flash('You must book at least 1 place.')
            elif placesRequired < 0:
                flash('The value cannot be negative.')
            else:
                flash('The value exceeds 12. Please reduce the value.')

        return render_template('booking.html', club=club, competition=competition)

    except ValueError:
        flash('Invalid number of places. Please enter a valid number.')
        return redirect(url_for('login'))

    except StopIteration:
        flash('Club or competition not found. Please try again.')
        return redirect(url_for('index'))

    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
