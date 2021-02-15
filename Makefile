install:
	pip install -e .['dev']

db:
	python .\ProjectFlaskSimble\prepara_banco.py
run:
	python .\ProjectFlaskSimble\jogoteca.py
