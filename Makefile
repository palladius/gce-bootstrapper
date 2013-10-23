
PROJECT_ID = 613126411804

clean:
	rm *.pyc */*.pyc

delete-test-instances:
	bin/gcutil-delete-all-by-name-matching "test-" "$(PROJECT_ID)"

gclb:
	./bootstrap.py gclb | tee out/out-gclb-`date +%s`.out

sample:
	./bootstrap.py sample | tee out/out-sample-`date +%s`.out

install:
	sudo easy_install importlib pyyaml
