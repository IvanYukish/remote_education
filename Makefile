bootstrap:
		$(VENV_PATH)/python ./crmpro/manage.py migrate;
up:
		docker-compose up
up-d:
		docker-compose up -d
stop-all:
		docker stop $(docker ps -aq)
down:
		docker-compose down




