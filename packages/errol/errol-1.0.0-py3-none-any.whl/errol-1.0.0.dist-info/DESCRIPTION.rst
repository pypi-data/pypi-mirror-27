# Errol

Errol is a file sender that rely on [inotify](https://en.wikipedia.org/wiki/Inotify). It can be used to watch a directory and automatically transfers the new files (or modified ones) with XMPP.

## Prerequisites

Errol needs the following requirements:

 * A system supporting [inotify](https://en.wikipedia.org/wiki/Inotify) (Linux).
 * an XMPP (jabber) account supporting the following XEPs: [Stream Management](https://xmpp.org/extensions/xep-0198.html), [Publish-Subscribe](https://xmpp.org/extensions/xep-0060.html), [Multi-User Chat](https://xmpp.org/extensions/xep-0045.html)
 * A pubsub service where the nodes can be set as open. The node name is defined in the configuration file. I personally  use [sat_pubsub](https://blog.agayon.be/sat_pubsub.html). A pubsub 
component developed for the project [Salut à Toi](https://salut-a-toi.org/). 
 * A Multi-User Chat because not all XMPP accounts support PubSub. For now, some information are still shared through MUC messages. This behavior could change in the future.

You can use your own XMPP server or choose a XMPP service among the following list.  
https://conversations.im/compliance/

#### Create the pubsub node

This step is optional if you already have a write access on the pubsub node. The following example use [jp](https://blog.agayon.be/sat_jp.html), the Salut à  Toi command-line interface but 
[slixmpp](https://dev.louiz.org/projects/slixmpp) or 
[sleekxmpp](https://github.com/fritzy/SleekXMPP) can be used. 

```
$ jp pubsub node create -f publish_model open be.agayon.errol:0 -s pubsub.agayon.be -c
```
The node name be.agayon.errol:0 is recommended in order to identify the functionnality.

As an example, there are the node options on the service pubsub.agayon.be:
```
$ jp pubsub node info be.agayon.errol:0 -s pubsub.agayon.be
persist_items: True
deliver_payloads: True
serial_ids: False
publish_model: open
access_model: open
send_last_published_item: on_sub
```


### Tests

You can test your setup with the examples scripts of [slixmpp](https://git.poez.io/slixmpp).

 * [pubsub_client.py](https://git.poez.io/slixmpp/tree/examples/pubsub_client.py)
 * [pubsub_events.py](https://git.poez.io/slixmpp/tree/examples/pubsub_events.py)
 * [s5b_receiver.py](https://git.poez.io/slixmpp/tree/examples/s5b_transfer/s5b_receiver.py)
 * [s5b_sender.py](https://git.poez.io/slixmpp/tree/examples/s5b_transfer/s5b_sender.py)

Example:
```
./s5b_file_sender.py -j jid@example.org -p pass -r john@example.org -f /path/to/file.txt 
```

See the scripts for more information.


## Getting started with Errol

First you need to clone the repository. 
Errol needs the following dependencies:

 * [slixmpp](https://dev.louiz.org/projects/slixmpp) (python 3 only)
 * [asyncio ](https://docs.python.org/3/library/asyncio.html)
 * [configparser](https://docs.python.org/3/library/configparser.html)
 * [aionotify](https://github.com/rbarrois/aionotify)

## Installing

You can install errol easily in a [virtualenv](https://virtualenv.pypa.io/en/stable/userguide/) or not:
```
 $ python3 setup.py install
```

On Archlinux:

```
A PKGBUILD will be available soon.
```

## Configuration

You need to provide information about the XMPP account.

```
$ cat config.example.ini

[XMPP]
pubsub=pubsub.example.org
node=be.agayon.errol:0
room=chat@chat.example.org
jid=jid@example.org/errol
password=pass
ressource_receiver=-receiver
ressource_sender=-
nick_sender=example_sender
nick_receiver=example_receiver
receiver=jid@example.org/errol-receiver
```

 * jid : the jabber account
 * password: the xmpp password
 * pubsub: the pubsub server (publish activity)
 * room: the MUC (chatroom) where errol display information.

The files will be sent by jid@example.org/errol-0 and received by jid@example.org/errol-receiver
. The nicks are the usernames used on the MUC.


## Running

Once installed, Errol can be launched in a terminal.

```
$ errol --help
usage: errol [-h] [-e EVENTS] [-f FILE] [-d] -p PATH -c COMMAND

Automatic XMPP file sender and directory watcher

optional arguments:
  -h, --help            show this help message and exit
  -e EVENTS, --events EVENTS
                        Number of events to watch (delete, create modify) in
                        the directory. Once reached, the program stops.
  -f FILE, --file FILE  Config file containing XMPP parameters
  -d, --debug           set logging to DEBUG
  -p PATH, --path PATH  The path watched.
  -c COMMAND, --command COMMAND
                        The executed command: xmpp or watcher
```

### On device A
If you want to watch the directory /tmp/sender, the following command can be used:

```
$ errol -f config.example.ini -p /tmp/sender -c watcher
```

All modified or new files created in the watched location will be sent by XMPP.

### On device B
If you want to receive the files, you have to launch Errol with the following command line.

```
$ errol -f config.example.ini -p /tmp/receiver -c xmpp
```

All the received files will be stored in the directory defined with the option '-p'.

## License

This project is licensed under the GPLv3 - see the [LICENSE.txt](https://gitlab.com/jnanar/errol/blob/master/LICENCE.txt) file for details

## Acknowledgments

 * [Slixmpp](https://github.com/poezio/slixmpp) for their nice library.
 * French XMPP community (sat@chat.jabberfr.org, jabberfr@chat.jabberfr.org)
 * Goffi from the [Salut à Toi](https://salut-a-toi.org/) project.


