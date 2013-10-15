
PROJECT_ID = 613126411804

clean:
	rm *.pyc */*.pyc

delete-test-instances:
	gcutil --project=$(PROJECT_ID) listinstances --format names | grep test | sed -e 's:/: :g' | cut -f 6 -d' ' | sort|  xargs echo Cut and paste this: gcutil --project $(PROJECT_ID) deleteinstance -f

load-balancer:
	./bootstrap.py load-balancer | tee out/out-`date +%s`.out
