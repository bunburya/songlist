# songlist

This is a very simple web application that lets any user add links to songs they like for others to see.  As well as this basic functionality, the songlist has the following features:

- a GET / POST API for (eg) IRC bot integration;

- an Atom feed to allow people to subscribe and keep up to date with latest additions to the list; and

- (in progress) a playlist feature where users can play songs from the list one after another from a single web page.

The songlist was created for the use of a small group of friends.  Anyone can remove any song; there aren't really any safeguards or authorisation requirements built in at the moment.

The songlist is written primarily in Python using the Flask framework.
