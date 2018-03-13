# Pylarm

Pylarm is a remote alerting tool. It is a python program that allows one to play a music file on an alarm server, by sending the appropriate command. It was conceived to help wake persons if they oversleep, or to notify people of any other arbitrary important happening.

### Protocol
The commands are build up by an action, followed by a token. For instance, to engage the alarm, the command should be the following, where *alarm* is the action and *_token123456* is the token.

```sh
b'alarm_token123456' 
```
The functions that are currently implemented, are:
- alarm - To engage the alarm
- stop - To stop the alarm
- info - To get information about the current state of the alarm 

The server sends a response after each command, except when an incorrect token was sent. It is possible to edit the server to send a warning after an incorrect token.

### Requirements
The server (as well as the optional client application) are written for Python 3.6. The server uses the [Pygame library] to play the alarm music. It also uses the datatime library. To install these elements:
```sh
$ pip3 install pygame datetime
```

### Configuration
The server is accompanied by a [configuration file]. The configuration allows changes for which address and port the server binds to. Also for which sound is to be played, as well as the moments in which the alarm is allowed to be engaged.

### Usage
After setting up the configuration file, the server should be started:
```sh
$ python3 pylarmServer.sh
```
If all goes well, the server should be ready to accept alarm triggers.

### Todos

 - Add an option in the config to change the times the alarm file plays.
 - Allow a client to make a difference between an infinitely playing alarm or an incidental one.

License
----

GPLv3

   [configuration file]: <http://link>
   [Pygame library]: <https://www.pygame.org/docs/>
