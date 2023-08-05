NetworX NX584/NX8E Interface Library and Server
===============================================

This is a tool to let you interact with your NetworX alarm panel via
the NX584 module (which is built into NX8E panels). You must enable it
in the configuration and enable the operations you want to be able to
do before this will work.

To install::

 # pip install pynx584

The server must be run on a machine with connectivity to the panel,
which can be a local serial port, or a Serial-over-LAN device (i.e. a
TCP socket). For example::

 # nx584_server --serial /dev/ttyS0 --baud 38400

or::

 # nx584_server --connect 192.168.1.101:23

Once that is running, you should be able to do something like this::

 $ nx584_client summary
 +------+-----------------+--------+--------+
 | Zone |       Name      | Bypass | Status |
 +------+-----------------+--------+--------+
 |  1   |    FRONT DOOR   |   -    | False  |
 |  2   |   GARAGE DOOR   |   -    | False  |
 |  3   |     SLIDING     |   -    | False  |
 |  4   | MOTION DETECTOR |   -    | False  |
 +------+-----------------+--------+--------+
 Partition 1 armed

 # Arm for stay with auto-bypass
 $ nx584_client arm-stay

 # Arm for exit (requires tripping an entry zone)
 $ nx584_client arm-exit

 # Auto-arm (no bypass, no entry zone trip required)
 $ nx584_client arm-auto

 # Disarm
 $ nx584_client disarm --master 1234

Config
------

The config.ini should be generated once the controller reports the first
zone name. However, here is a full config.ini if you want to pre-populate
it with zone names:

 [config]
 # max_zone is the highest numbered zone you have populated
 max_zone = 5

 # Set to true if your unit sends DD/MM dates instead of MM/DD
 euro_date_format = False
 
 [email]
 fromaddr = security@foo.com
 smtphost = imap.foo.com
 
 [zones]
 # Zone names
 1 = Front Door
 2 = Garage Entry
 3 = Garage Side
 4 = Garage Back
 5 = Kitchen
