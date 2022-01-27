# ubutton

A MicroPython class for dealing with gpio inputs. Specifically pushbutton presses.  It includes detection of "short" and "long" press, click counting, debouncing, and callbacks for each type of event.
Doesn't rely on 'Timer' or 'Delay' methods.

## Usage

Usage is simple. Just create an instance of `ubutton` class and specify callbacks for each required event type. A simple usage example is presented in the main.py.

It is assumed the gpios are pulled down externally and that pressing the button will shorten the input to a high level.
