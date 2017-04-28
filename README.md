[![Build Status](https://travis-ci.org/akurihara/impulse.svg?branch=master)](https://travis-ci.org/akurihara/impulse)

Impulse
=======

If you enjoy going to concerts or sporting events, you know that prices on the secondary ticket market can be painfully higher than face value. If ticket resellers overestimate demand, however, it's possible for ticket prices to drop significantly on the day of an event. Impulse helps you take advantage of this phenomenon by letting you decide what price you're willing pay for an event, and notifying you if ticket prices fall below that amount.

Running Locally
===============

1. Create a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing dependencies of this project.

2. Start the server.

```
pip install -r requirements.txt
python manage.py runserver
```

3. Navigate your browser to `127.0.0.1:8000`

Live Demo
=========

See the app in action with live Seatgeek and Twilio functionality here:
https://impulse-tickets.herokuapp.com/events
