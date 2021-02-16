# Monitor-Cyber-defence

Program structure:
The program is built as a hashmap (or a dictionary). Each date is the key and the values are process ID and process name, split by commas.
The program is cross platform meaning it’s monitoring services in both Windows system and Linux (Ubuntu distribution) system.
Used libraries:
from __future__: With_statemet- in some part in the program I used with statement to access files in a more convenient way.

from ast: literal_eval: to access the specific key in the hash map.

datetime, time- for current timestamp while writing and reading to and from files.

watchdog, logging- for the program’s protection against file changes and modifications.

psutil- for iterating over running processes in system

Data structures:
Hash map- for running processes. Allowed me to search for specific dates in manual mode more easily.
List- to hold all different values between two hash maps in manual mode.
UI:
There is a main menu to ease choosing from the user’s options. Every time she/he wish to go back to it she/he can press Ctrl+c.
There is an option for quitting, but after pressing it once the user will be transferred to the Watchdog* and must press Ctrl+c again.

Defending from hackers:
*Watchdog- my implementation of defending from hackers. 
I used Python’s library called Watchdog that observes and listens any changes and modifications to files. It alerts about it to user by printing to screen: which file was changed (modifids, created and deleted) and what time it happened.
Obviously the user wouldn’t want to change files after the program finished (if she/he would like so- the alert would be irrelevant and they can ignore it) so this mechanism is useful for us to detect hackers actions on our files- if there are any.


