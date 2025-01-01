.PHONY: install poetry-env install-deps migrate runserver livereload tailwind-install tailwind-build build-and-run setup

# Install Poetry
install:
	curl -sSL https://install.python-poetry.org | python3 -

# Spawn Poetry virtual environment
poetry-env:
	poetry shell

# Install dependencies
install-deps:
	poetry install

# Run database migrations
migrate:
	python manage.py migrate

# Start the Django server
runserver:
	python manage.py runserver

# Start the Django server with livereload
livereload:
	python manage.py livereload

# Install Node.js packages for Tailwind
tailwind-install:
	npm install

# Run Tailwind build watcher
tailwind-build:
	npm run twbuild

# Build the project and run the server (supports --livereload)
build-and-run:
	@echo "Running build process..."
	@$(MAKE) migrate
	@if [ "$(arg)" = "--livereload" ]; then \
		$(MAKE) livereload; \
	else \
		$(MAKE) runserver; \
	fi

# Set up Poetry and the Python environment
setup:
	@echo "Setting up Poetry and the Python environment..."
	@$(MAKE) install
	@$(MAKE) install-deps
