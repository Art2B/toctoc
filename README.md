toctoc
======

A collection of scripts to run a twitter doorbell on a Raspberry Pi
Here is a tutorial of the [doorbell](https://github.com/soixantecircuits/toctoc/blob/master/Overview.md)

If you're just interested in the autossh-remote:
```
$ git clone https://github.com/soixantecircuits/toctoc.git
$ cd toctoc/remotecontrol
$ python install_autossh.py
```

# Enable DMX Button #

The following only directly work in our studio. Please send me a message if you want some informations to customize.

```
$ cd toctoc/tests/
$ screen -S pushButton
$ sudo python push-button.py
```

When you want to turn off the light, execute those commands:

```
$ screen -r pushButton
Ctrl + C
$ sudo python stop-lights.py
exit
```

Here is the basic to the lights !

