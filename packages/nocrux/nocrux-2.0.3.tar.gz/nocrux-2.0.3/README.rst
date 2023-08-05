nocrux
======

Nocrux is an easily configurable daemon manager that can be used by any
user on the system. It uses double-forks to transfer cleanup
responsibility of daemons to the init process.

-  `Synopsis <#synopsis>`__
-  `Requirements <#requirements>`__
-  `Installation <#installation>`__
-  `A note about child processes <#a-note-about-child-processes>`__
-  `A note about managing daemons under a different
   user <#a-note-about-managing-daemons-under-a-different-user>`__
-  `Changelog <#changelog>`__

Synopsis
--------

::

    usage: nocrux [-h] [-e] [-l] [-f] [--sudo] [--as AS_] [--stderr] [--version]
                  [daemon] [command]

      Nocrux is a daemon process manager that is easy to configure and can
      operate on the user- or root-level. The nocrux configuration syntax is
      similar to Nginx. All users configuration file is in ~/.nocrux/conf,
      except for the root user, which is in /etc/nocrux/conf.
      
      This will start your $EDITOR to open the configuration file:
      
          $ nocrux -e
      
      The main namespace has the options and default values below:
      
          root ~/.nocrux/run;
          kill_timeout 10;
      
      You can also include other files like this (relative paths are considered
      relative to the configuration file):
      
          include ~/more-nocrux-config.txt;
      
      To configure a new daemon, you start a `daemon` section, specify the name
      and then the daemon's options in the news scope.
      
          daemon jupyter {
            cwd ~;
            run jupyter notebook;
          }
      
      You can now start the daemon with:
      
          $ nocrux jupyter start
          [nocrux]: (jupyter) starting "jupyter notebook"
          [nocrux]: (jupyter) started (pid: 10117)
      
      The following commands are available for all daemons:
      
        - start
        - stop
        - restart
        - status
        - pid
        - cat
        - tail
      
      You can specify additional commands like this:
      
          daemon jupyter {
            cwd ~;
            run jupyter notebook;
            command uptime echo $(($(date +%s) - $(date +%s -r $DAEMON_PIDFILE))) seconds;
          }
      
      Now to run this command:
      
          $ nocrux jupyter uptime;
          3424 seconds;
      
      Here's a daemon configuration with all available options and the
      respective default or example values:
      
          daemon test {
            # Example values:
            export PATH=/usr/sbin:$PATH;
            export DEBUG=1;
            run ~/Desktop/mytestdaemon.sh arg1 "arg 2";
            cwd ~;
            command uptime echo $(($(date +%s) - $(date +%s -r $DAEMON_PIDFILE))) seconds;
            requires daemon1 daemon2;
      
            # Options with their respective defaults:
            user me;
            group me;
            stdin /dev/null;
            stdout $root/$name.out;
            stderr $stdout;
            pidfile $root/$name.pid;
            signal term TERM;
            signal kill KILL;
          }

    positional arguments:
      daemon        The name of the daemon.
      command       A command to execute on the specified daemon.

    optional arguments:
      -h, --help    show this help message and exit
      -e, --edit    Edit the nocrux configuration file.
      -l, --list    List up all daemons and their status.
      -f, --follow  Pass -f to the tail command.
      --sudo        Re-invoke the same command with sudo.
      --as AS_      Run the command as the specified user. Overrides --sudo.
      --stderr      Choose stderr instead of stdout for the cat/tail command.
      --version     Print the nocrux version and exit.

Requirements
------------

-  Unix-like OS (tested on Ubuntu 15-17, Debian Jessie, macOS Sierra)
-  Python 3.4+
-  `Node.py <https://nodepy.org>`__ (optional)

Installation
------------

::

    $ pip3 install --user nocrux    # or
    $ nodepy-pm install git+https://github.com/NiklasRosenstein/nocrux.git@v2.0.3 --global

A note about child processes
----------------------------

Nocrux can only send SIGTERM or SIGKILL to the **main process** that it
originally started. If that process spawns any child precesses, it must
take care of forwarding the signal! The thread `*Forward SIGTERM to
child in Bash* <http://unix.stackexchange.com/q/146756/73728>`__
contains some information on doing that for Bash scripts. For very
simple scripts that just set up an environment, I recommend the ``exec``
approach as described in the link.

A note about managing daemons under a different user
----------------------------------------------------

Example:

::

    daemon gogs {
      user gogs;
      cwd /home/gogs/gogs;
      run ./gogs web;
    }

If you're trying to manage a daemon that will be started by nocrux under
a different user, you need the permissions to do so. For example, the
superuser is allowed to do so and using nocrux as root should work
immediately.

However, if you are not already the root user, nocrux will by default
try to re-run itself as the user specified in the daemon, eg. in this
case:

::

    sudo gogs NOCRUX_CONFIG=/home/niklas/.nocrux/conf /home/niklas/.local/bin/nocrux gogs start

This will only work if

1. You installed nodepy system-wide, **or** you installed it with
   Node.py and the ``gogs`` user can read the path of the nocrux
   executable and the nocrux package directory
2. The ``gogs`` user can read your nocrux configuration file

Otherwise, you may be greeted with one of the following error messages:

-  sudo: unable to execute /home/niklas/.local/bin/nocrux: Permission
   denied
-  pkg\_resources.DistributionNotFound: The 'nocrux==2.0.3' distribution
   was not found and is required by the application
-  ModuleNotFoundError: No module named 'nodepy'

Changelog
---------

**v2.0.3**

-  Update for Node.py 2
-  Add ``--sudo`` command-line option
-  Add ``--as <user>`` command-line option
-  Add support for variable substition in the ``daemon { export; }``
   field
-  Add support for custom signals for termination and killing a daemon
   process (see issue #21)
-  Add support for custom daemon subcommands that have access to the
   following environment variables: ``$DAEMON_PID``,
   ``$DAEMON_PIDFILE``, ``$DAEMON_STDOUT``, ``$DAEMON_STDERR`` (see
   issue #22)
-  Add support for ``daemon{ root; }`` field which will change the
   parent directory of the default paths for the PID and standard output
   files
-  Add support for ``#`` comments in the configuration file
-  Change behaviour of ``daemon { user; }`` option, now serves as a
   default value for the ``--as`` option
-  Fix configuration loading (``daemon { run; }`` may now be preceeded
   by any other option)
-  Fix ``-e, --edit`` now opens the editor always for the user's file

**v2.0.2**

-  fix ``nocrux version`` command
-  add ``nocrux edit`` command
-  order of daemons when referencing them with ``all`` is now sorted
   alphabetically

**v2.0.1**

-  removed ``fn:out``, ``fn:err`` and ``fn:pid`` commands (actually
   already removed in 2.0.0)
-  the default ``root`` config value will now be ``/var/run/nocrux`` if
   the configuration file is loaded from ``/etc/nocrux/conf``
-  more sophisticated config file parsing with ``nr.parse.strex`` module
-  update error message hinting to check output of
   ``nocrux <daemon> tail`` if daemon could not be started

**v2.0.0**

-  cli is now ``nocrux <daemon> <command>`` (switched)
-  to specify multiple daemons, the ``<daemon>`` argument can be a list
   of comma separated daemon names
-  configuration file is no longer a Python script
-  configuration file must now be located at ``~/.nocrux/conf`` or
   ``/etc/nocrux/conf``
-  nocrux can now be installed via Node.py
-  add support for defining per-process environment variables

**v1.1.3**

-  update ``README.md`` (corrected example and command-line interface)
-  remove unusued ``-e, --stderr`` argument
-  fix ``setup.py`` (use ``py_modules`` instead of the invalid
   ``modules`` parameter)
-  enable running ``nocrux.py`` directly without prior installation
-  add ``pid``, ``tail``, ``tail:out`` and ``tail:err`` subcommands

**v1.1.2**

-  add ``setup.py`` installation script, remove ``nocrux`` script
-  update ``README.md`` and renamed from ``README.markdown``

**v1.1.1**

-  close #18: Automatically expand prog ~ before starting process
-  fix #17: PID file not deleted after daemon stopped
-  close #16: Tail command is counter intuitive
-  update output of command-line program
-  process exit code is now printed to daemon standard error output file
-  fixed stopping multiple daemons when one wasn't running
-  implement #10: daemon dependencies

**v1.1.0**

-  Renamed to ``nocrux``
-  Update README and command-line help description

**v1.0.1**

-  Add ``krugs tail <daemon> [-e/-stderr]`` command
-  Add special deaemon name ``all``
-  Fix ``krugs restart`` command
