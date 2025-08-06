# Docker Compose wrapper
DC = docker compose

up:
	sudo $(DC) up -d

down:
	sudo $(DC) down --volumes --remove-orphans
	sudo docker network prune -f
