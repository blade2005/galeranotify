galeranotify
============

Python E-Mail script for use with Galera wsrep_notify_cmd

Why do I need / want this?
--------------------------

[Galera](http://codership.com/products/galera_replication) makes my life easier with near synchronous replication for MySQL.  We have monitoring tools in place, but its nice to get updates in real time about how the cluster is operating.  So I wrote galeranotify.

I've been using this on our [Percona XtraDB Cluster](http://www.percona.com/software/percona-xtradb-cluster) for quite a while now with no issues.

I hope someone finds it useful.

Set up
------

1. Copy to /usr/local/bin 

2. Copy galeranotify.conf to /etc.

3. Change the galeranotify.conf to suit your needs

4. Test run of your settings to ensure it is working and you are receiving emails.

5. Set 'wsrep_notify_cmd = <path of galeranotify.py>' in your my.cnf file.

6. Restart MySql.

SELinux
-------

A SELinux policy (galeranotify.pp) is also included that allows the mysql user to connect to a standard remote smtp port (port 25).  If you are using an alternate SMTP port (common with SSL), this rule will not work for you.

Usage:

    semodule -i galeranotify.pp

This rule was generated on Centos 6.4 64-bit.  It may or may not work for your particular setup.
