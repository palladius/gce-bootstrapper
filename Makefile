
clean:
	rm *.pyc */*.pyc

delete-test-instances:
	PROJECT_ID=613126411804
	gcutil --project=$PROJECT_ID listinstances --format names | grep test | sed -e 's:/: :g' | awk '{print $6}' | xargs echo Cut and paste this: gcutil --project $PROJECT_ID deleteinstance -f
