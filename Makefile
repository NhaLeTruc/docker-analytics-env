# Docker Compose wrapper
DC = docker compose



spark_submit:
	docker exec spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./opt/bitnami/spark/apps$(app)
