gce-bootstrapper
----------------

This is my first Google Compute Engine project. I use it to configure/bootstrap my machines,
based on projects.

Try this:

    cp config.yml.dist config.yml
    vi config.yml                   # Edit with your project configuration
    ./bootstrap.py  <PROJECT_NAME>  # (e.g. "load-balancer")

Build your own project
----------------------

To build your own application, please follow the structure of my projects like this:

    export PROJ=foobar
	mkdir projects/$PROJ.d/
	touch projects/sample.py projects/$PROJ.py


Code
----

This code is published here:

* https://github.com/palladius/gce-bootstrapper


Thanks
------

My mum.
