jupyter:
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''
tensorboard:
	tensorboard --logdir=./logs --host=0.0.0.0 --port=6006
mlflow:
	mlflow ui --host=0.0.0.0 --port=5000
streamlit:
	streamlit run app.py --server.port=8501 --server.address=0.0.0.0

.PHONY: jupyter tensorboard mlflow streamlit