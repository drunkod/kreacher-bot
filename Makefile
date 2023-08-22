# create virtual enviroment ro run the bot
create_env:
	virtualenv kreacher_env

#  build in docker container
docker_build:
	docker build . -t kreacher

# run docker container
docker_run:
	docker run kreacher

# install deps required to run this project
install:
	pip3 install --no-deps -U pytgcalls==3.0.0.dev24 tgcalls==3.0.0.dev6 && pip3 install -r requirements.txt

# format files in the project
format:
	black . --line-length 79

# lint all project looking for issues
lint:
	pylint --recursive yes --jobs=4 .

# generate string session of your telegram account
session_string:
	python3 ./session/session.py

# command to run bot in normal mode
run_bot:
	python3 -m bot

# command to run bot in virtual enviroment
run_virtual env:
	make_create env && make install && source kreacher_env/bin/activate && bash python3 -m kreacher

