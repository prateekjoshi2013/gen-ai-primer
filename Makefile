jupyter:
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''
tensorboard:
	tensorboard --logdir=./logs --host=0.0.0.0 --port=6006
mlflow:
	mlflow ui --host=0.0.0.0 --port=5000
streamlit:
	streamlit run app.py --server.port=8501 --server.address=0.0.0.0
ollama-fastapi:
	uvicorn ollama_fastapi.server:app --host 0.0.0.0 --port 8000
ollama-fastapi-dev:
	uvicorn ollama_fastapi.server:app --host 0.0.0.0 --port 8000 --reload
hf-fastapi:
	uvicorn hugging_face.server:app --host 0.0.0.0 --port 8000
hf-fastapi-dev:
	uvicorn hugging_face.server:app --host 0.0.0.0 --port 8000 --reload

.PHONY: jupyter tensorboard mlflow streamlit ollama-fastapi ollama-fastapi-dev hf-fastapi hf-fastapi-dev