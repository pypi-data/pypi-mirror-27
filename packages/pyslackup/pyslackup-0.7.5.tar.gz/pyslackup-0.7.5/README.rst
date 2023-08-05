*******
slackup
*******

Slackup is a simple CLI Slack client.
It supports reading config from a config file, from environment variables and from parameters passed directly to the script.

Slackup will read from file if one is passed with ``-f``. If both "message" and file is specified, file input takes precedence. Use ``-f -`` to read from STDIN.

======
Config
======
``~/.slackup.cfg`` or ``/etc/slackup.cfg`` will be read if they exist. ``~/.slackup.cfg`` takes precedence if it is found.

::

    slack_token: 'xoxp-YOUR-TOKEN-HERE'
    slack_channel: '#slackup'
    slack_username: 'slackup'
    slack_emoji: ':robot_face:'

Config can also be specified via environment variables. These will override config file entries if present:

::

    SLACK_TOKEN
    SLACK_CHANNEL
    SLACK_USERNAME
    SLACK_EMOJI
    SLACK_MESSAGE


=====
Usage
=====
::

    usage: slackops [-h] [-v] [-c CHANNEL] [-t TOKEN] [-u USERNAME] [-s] [-f FILE] [message]
    
    positional arguments:
      message               message to post to slack
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      -c CHANNEL, --channel CHANNEL
                            specify channel to post to
      -t TOKEN, --token TOKEN
                            set token to use
      -u USERNAME, --username USERNAME
                            set Slack username to post as
      -s, --snippet         Post message as attachment/snippet
      -f FILE, --file FILE  read message from file or stdin


========
Examples
========
::

    # Command line usage example
    echo 'HELLO' | slackops -c 'someotherchannel' -f -
    slackops "greetings fellow kids"
    slackops -s -f inputfile.txt

    # ...or used as a python module
    from slackup import SlackUp
    s = SlackUp()
    s.post("ehlo world")
