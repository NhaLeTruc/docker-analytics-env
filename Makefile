# Docker Compose wrapper
DC = docker compose

up:
	sudo $(DC) up -d

down:
	sudo $(DC) down --volumes --remove-orphans
	sudo docker network prune -f

deep_clean:
	sudo $(DC) down --volumes --remove-orphans
	sudo docker network prune -f
	sudo docker builder prune -fa

spark_submit:
	sudo docker exec spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./opt/bitnami/spark/apps$(app)

run-scaled:
	make down && docker-compose up --scale spark-worker=3
