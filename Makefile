DEFAULT_GOAL := run
run:
	@python3 -m streamlit run main.py;
run2:
	@python3 -m streamlit run main.py --server.port 8502
lab:
	@python3 lab.py;
