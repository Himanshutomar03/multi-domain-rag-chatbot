@echo off
set PROJECT=multi-domain-rag-chatbot

echo Creating project: %PROJECT%

mkdir %PROJECT%
cd %PROJECT%

rem Top-level files
type nul > README.md
type nul > requirements.txt
type nul > .gitignore

rem Config
mkdir config
type nul > config\settings.yaml
type nul > config\prompts_legal.txt
type nul > config\prompts_medical.txt
type nul > config\prompts_education.txt
type nul > config\model_config.json

rem Data folders
mkdir data
mkdir data\raw
mkdir data\raw\legal
mkdir data\raw\medical
mkdir data\raw\education

mkdir data\processed
mkdir data\processed\legal
mkdir data\processed\medical
mkdir data\processed\education

rem Notebooks
mkdir notebooks
type nul > notebooks\01_explore_legal.ipynb
type nul > notebooks\02_explore_medical.ipynb
type nul > notebooks\03_explore_education.ipynb
type nul > notebooks\04_evaluation.ipynb

rem Source folders
mkdir src
type nul > src\__init__.py

mkdir src\data_preparation
type nul > src\data_preparation\__init__.py
type nul > src\data_preparation\preprocess_legal.py
type nul > src\data_preparation\preprocess_medical.py
type nul > src\data_preparation\preprocess_education.py
type nul > src\data_preparation\clean_text.py

mkdir src\embeddings
type nul > src\embeddings\__init__.py
type nul > src\embeddings\create_embeddings.py
type nul > src\embeddings\vector_store_legal.py
type nul > src\embeddings\vector_store_medical.py
type nul > src\embeddings\vector_store_education.py

mkdir src\retriever
type nul > src\retriever\__init__.py
type nul > src\retriever\domain_router.py
type nul > src\retriever\hybrid_search.py
type nul > src\retriever\reranker.py

mkdir src\rag_pipeline
type nul > src\rag_pipeline\__init__.py
type nul > src\rag_pipeline\build_rag_chain.py
type nul > src\rag_pipeline\answer_generator.py

mkdir src\evaluation
type nul > src\evaluation\__init__.py
type nul > src\evaluation\test_questions_legal.json
type nul > src\evaluation\test_questions_medical.json
type nul > src\evaluation\test_questions_education.json
type nul > src\evaluation\evaluate_rag.py

mkdir src\app
type nul > src\app\__init__.py
type nul > src\app\main.py
type nul > src\app\ui_streamlit.py

rem Vector stores
mkdir vectorstores
mkdir vectorstores\legal_faiss
mkdir vectorstores\medical_faiss
mkdir vectorstores\education_faiss

rem Deployment
mkdir deployment
type nul > deployment\dockerfile
type nul > deployment\docker-compose.yaml
type nul > deployment\run.sh

echo Project structure created successfully!

