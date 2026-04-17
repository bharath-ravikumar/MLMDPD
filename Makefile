.PHONY: help install run lint clean

help:
	@echo "Common Makefile commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run main script"
	@echo "  make lint      - Lint code with flake8"
	@echo "  make clean     - Remove build artifacts"

install:
	pip install -e .[dev]

run:
	python src/packages/run_MLMDPD.py

lint:
	flake8 src/packages

clean:
	rm -rf build dist .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf *.egg-info
