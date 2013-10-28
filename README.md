gce-bootstrapper
----------------

gce-bootstrapper (codename `bootsy`) is my first Google Compute Engine project. I use it to configure/bootstrap my machines,
based on the concept of `addons`. Note that this is a very rudimental script, if you need to do anything more complex, you
might want to use a proper config Management system (eg Puppet, Chef, ..): these two for sure have good modules for GCE.

Try this:

    cp config.yml.dist config.yml
    vi config.yml                       # Edit with your project configuration
    ./bootstrap.py  <ADDON_NAME>        # (e.g. "load-balancer")

Build your own project
----------------------

To build your own application, please follow the structure of my projects like this:

	export ADDON=foobar
	mkdir projects/$ADDON.d/
	touch projects/sample.py projects/$ADDON.py

Install
-------

To get the code up and running, you might need to install the following python packages.
See `Makefile` for this.

Code
----

This code is published here:

* https://github.com/palladius/gce-bootstrapper


Thanks
------

My mum.
