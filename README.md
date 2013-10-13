gce-bootstrapper
----------------

This is my first Google Compute Engine project. I use it to configure/bootstrap my machines,
based on projects.

Try this:

    `cp config.yml.dist config.yml`
    `vi config.yml`  # Edit with your project configuration
    `./bootstrap.py`

BUILD YOUR OWN PROJECT
----------------------

To build your own application, please follow the structure of my projects like this:

	mkdir projects/MYPROJECT/
	cp projects/sakura.py projects/MYPROJECT.py

TODO
----

See TODO file.


Code
----

This code is published here:

* https://github.com/palladius/gce-bootstrapper


Docs
====

The docs are here (Google only):

* https://sites.google.com/a/google.com/cloud-support/compute-engine/projects/gce-provisioner

In order to publish stuff, you should:

* remove personal stuff from var/ and tmp/
* remove passwords from your scripts. I'm slowly moving in Sakura passwords from script to metadata

Thanks
------

My mum.
