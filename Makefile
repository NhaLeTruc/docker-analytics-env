# Docker Compose wrapper
DC = docker compose

# run_airflow_help: 
# 	$(DC) run airflow-cli "--help"

spark_submit:
	docker exec spark spark-submit --master spark://spark:7077 --deploy-mode client ./apps/$(app)
