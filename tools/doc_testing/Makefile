# Makefile for MicroPython Documentation Sample Testing
#
# This Makefile provides convenient commands for extracting and testing
# code samples from MicroPython documentation.

# Configuration
DOCS_PATH ?= ../../docs
OUTPUT_PATH ?= organized_samples
MICROPYTHON_STUBS_PATH ?= ./micropython-stubs
PYTHON ?= python3
# Get the directory where this Makefile is located
MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
# Root directory is two levels up from tools/doc_testing
ROOT_DIR := $(MAKEFILE_DIR)../..

# Detect OS for command compatibility
ifeq ($(OS),Windows_NT)
    # Windows/MinGW commands
    RM = del /q
    RMDIR = rmdir /s /q
    MKDIR = mkdir
    FIND_PY_COUNT = @if exist $(OUTPUT_PATH) (for /f %%i in ('dir /b /s $(OUTPUT_PATH)\*.py 2^>nul ^| find /c ".py"') do @echo %%i) else echo 0
    FIND_PLATFORM = @if exist $(OUTPUT_PATH) (for %%p in (esp32 esp8266 rp2 pyboard wipy unix stm32 samd mimxrt renesas-ra zephyr) do @(for /f %%i in ('dir /b $(OUTPUT_PATH)\*%%p*.py 2^>nul ^| find /c ".py"') do @if not %%i==0 echo   %%p: %%i))
else
    # Unix commands
    RM = rm -f
    RMDIR = rm -rf
    MKDIR = mkdir -p
    FIND_PY_COUNT = find $(OUTPUT_PATH) -name '*.py' 2>/dev/null | wc -l
    FIND_PLATFORM = for platform in esp32 esp8266 rp2 pyboard wipy unix stm32 samd mimxrt renesas-ra zephyr; do \
		count=$$(find $(OUTPUT_PATH) -name "*$$platform*" -name "*.py" 2>/dev/null | wc -l); \
		if [ $$count -gt 0 ]; then echo "  $$platform: $$count"; fi; done
endif

# Colors for output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

.PHONY: help setup clean extract-samples test-samples test-samples-full stats install-deps
.PHONY: lint format check-format ci-test docker-test

help: ## Show this help message
	@echo "MicroPython Documentation Sample Testing"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "Configuration:"
	@echo "  DOCS_PATH=$(DOCS_PATH)"
	@echo "  OUTPUT_PATH=$(OUTPUT_PATH)"
	@echo "  MICROPYTHON_STUBS_PATH=$(MICROPYTHON_STUBS_PATH)"

setup: ## Set up the development environment
	@echo "$(GREEN)Setting up development environment...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install pytest pyyaml mypy astroid ruff
	@if [ ! -d "$(MICROPYTHON_STUBS_PATH)" ]; then \
		echo "$(YELLOW)Cloning micropython-stubs...$(NC)"; \
		git clone https://github.com/josverl/micropython-stubs.git $(MICROPYTHON_STUBS_PATH); \
		cd $(MICROPYTHON_STUBS_PATH) && \
		if [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then \
			$(PYTHON) -m pip install -e .; \
		fi; \
	else \
		echo "$(GREEN)micropython-stubs already exists$(NC)"; \
	fi
	@echo "$(GREEN)Setup complete!$(NC)"

install-deps: ## Install Python dependencies
	$(PYTHON) -m pip install pytest pyyaml mypy astroid ruff

extract-samples: ## Extract code samples from documentation
	@echo "$(GREEN)Extracting code samples from $(DOCS_PATH)...$(NC)"
	$(PYTHON) extract_doc_samples.py $(DOCS_PATH) --output $(OUTPUT_PATH) --stats
	@echo "$(GREEN)Extraction completed!$(NC)"

extract-samples-with-fixes: ## Extract samples including fixed syntax errors
	@echo "$(GREEN)Extracting code samples with syntax error fixes from $(DOCS_PATH)...$(NC)"
	$(PYTHON) extract_doc_samples.py $(DOCS_PATH) --output $(OUTPUT_PATH) --include-syntax-errors --stats
	@echo "$(GREEN)Extraction with fixes completed!$(NC)"

analyze-structure: ## Analyze and display the organized sample structure
	@if [ ! -d "$(OUTPUT_PATH)" ]; then \
		echo "$(YELLOW)No samples found, extracting first...$(NC)"; \
		$(MAKE) extract-samples; \
	fi
	@echo "$(GREEN)Analyzing sample structure...$(NC)"
	$(PYTHON) analyze_structure.py --samples-dir $(OUTPUT_PATH)

extract-samples-platform: ## Extract samples for specific platform (usage: make extract-samples-platform PLATFORM=esp32)
	@if [ -z "$(PLATFORM)" ]; then \
		echo "$(RED)Error: PLATFORM not specified. Usage: make extract-samples-platform PLATFORM=esp32$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Extracting $(PLATFORM) samples...$(NC)"
	$(PYTHON) extract_doc_samples.py $(DOCS_PATH) \
		--output $(OUTPUT_PATH) --stats --platform $(PLATFORM)

test-samples: ## Test extracted code samples (basic syntax and import checks)
	@if [ ! -d "$(OUTPUT_PATH)" ]; then \
		echo "$(YELLOW)No samples found, extracting first...$(NC)"; \
		$(MAKE) extract-samples; \
	fi
	@echo "$(GREEN)Running basic tests on code samples...$(NC)"
	cd $(OUTPUT_PATH) && $(PYTHON) -m pytest -v \
		--tb=short \
		--micropython-stubs-path=../$(MICROPYTHON_STUBS_PATH) \
		-p ../pytest_docsamples.py \
		--disable-warnings \
		.

test-samples-full: ## Test with full analysis (static analysis + execution)
	@if [ ! -d "$(OUTPUT_PATH)" ]; then \
		echo "$(YELLOW)No samples found, extracting first...$(NC)"; \
		$(MAKE) extract-samples; \
	fi
	@echo "$(GREEN)Running full analysis on code samples...$(NC)"
	cd $(OUTPUT_PATH) && $(PYTHON) -m pytest -v \
		--tb=short \
		--micropython-stubs-path=../$(MICROPYTHON_STUBS_PATH) \
		-p ../pytest_docsamples.py \
		--run-static-analysis \
		--run-execution-test \
		--disable-warnings \
		.

test-samples-platform: ## Test samples for specific platform (usage: make test-samples-platform PLATFORM=esp32)
	@if [ -z "$(PLATFORM)" ]; then \
		echo "$(RED)Error: PLATFORM not specified. Usage: make test-samples-platform PLATFORM=esp32$(NC)"; \
		exit 1; \
	fi
	@if [ ! -d "$(OUTPUT_PATH)" ]; then \
		echo "$(YELLOW)No samples found, extracting first...$(NC)"; \
		$(MAKE) extract-samples; \
	fi
	@echo "$(GREEN)Testing $(PLATFORM) samples...$(NC)"
	cd $(OUTPUT_PATH) && $(PYTHON) -m pytest -v \
		--tb=short \
		--micropython-stubs-path=../$(MICROPYTHON_STUBS_PATH) \
		-p ../pytest_docsamples.py \
		--platform-filter=$(PLATFORM) \
		--disable-warnings \
		.

stats: ## Show statistics about extracted samples
	@if [ -d "$(OUTPUT_PATH)" ]; then \
		echo "$(BLUE)Sample Statistics:$(NC)"; \
		echo "Total samples: $$($(PYTHON) -c "import pathlib; print(len(list(pathlib.Path('$(OUTPUT_PATH)').glob('*.py'))))"); \
		echo ""; \
		echo "$(BLUE)By platform:$(NC)"; \
		$(PYTHON) -c "import pathlib; samples = list(pathlib.Path('$(OUTPUT_PATH)').glob('*.py')); platforms = {}; [platforms.setdefault(p.name.split('_')[0], 0) or platforms.update({p.name.split('_')[0]: platforms[p.name.split('_')[0]] + 1}) for p in samples if '_' in p.name]; [print(f'  {k}: {v}') for k, v in sorted(platforms.items()) if v > 0]"; \
		echo ""; \
		echo "$(BLUE)Sample size distribution:$(NC)"; \
		$(PYTHON) -c "import pathlib; samples = list(pathlib.Path('$(OUTPUT_PATH)').glob('*.py')); lines = [len(open(f).readlines()) for f in samples]; small = len([l for l in lines if l <= 10]); medium = len([l for l in lines if 10 < l <= 50]); large = len([l for l in lines if l > 50]); print('Lines | Count'); print(f'1-10  | {small}'); print(f'11-50 | {medium}'); print(f'50+   | {large}')"; \
	else \
		echo "$(YELLOW)No samples directory found. Run 'make extract-samples' first.$(NC)"; \
	fi

clean: ## Clean up generated files
	@echo "$(YELLOW)Cleaning up generated files...$(NC)"
ifeq ($(OS),Windows_NT)
	@if exist $(OUTPUT_PATH) $(RMDIR) $(OUTPUT_PATH)
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
	@del /s /q *.pyc 2>nul
else
	$(RMDIR) $(OUTPUT_PATH)
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
endif
	@echo "$(GREEN)Cleanup complete$(NC)"

lint: ## Run linting on the doc testing tools
	@echo "$(GREEN)Running linting with ruff...$(NC)"
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy . --ignore-missing-imports

format: ## Format code using ruff
	@echo "$(GREEN)Formatting code with ruff...$(NC)"
	$(PYTHON) -m ruff format .

check-format: ## Check if code is properly formatted
	@echo "$(GREEN)Checking code formatting with ruff...$(NC)"
	$(PYTHON) -m ruff format --check .

ci-test: ## Run CI-style tests
	@echo "$(GREEN)Running CI tests...$(NC)"
	$(MAKE) clean
	$(MAKE) extract-samples
	$(MAKE) test-samples
	@echo "$(GREEN)CI tests completed successfully!$(NC)"

test-extraction: ## Test the extraction tool itself
	@echo "$(GREEN)Testing extraction tool...$(NC)"
	$(PYTHON) -m pytest tests/ -v

# Docker-based testing (if available)
docker-test: ## Run tests in Docker container
	@if command -v docker >/dev/null 2>&1; then \
		echo "$(GREEN)Running tests in Docker...$(NC)"; \
		docker run --rm -v $$(pwd):/workspace -w /workspace python:3.10 \
			bash -c "make setup && make ci-test"; \
	else \
		echo "$(RED)Docker not available, skipping Docker tests$(NC)"; \
	fi

# Development helpers
dev-setup: ## Setup for development with additional tools
	$(MAKE) setup
	$(PYTHON) -m pip install ruff mypy pre-commit
	@if [ -f ".pre-commit-config.yaml" ]; then \
		pre-commit install; \
	fi

watch-docs: ## Watch docs directory and re-extract samples on changes (requires entr)
	@if command -v entr >/dev/null 2>&1; then \
		echo "$(GREEN)Watching $(DOCS_PATH) for changes...$(NC)"; \
		find $(DOCS_PATH) -name "*.rst" | entr -r make extract-samples; \
	else \
		echo "$(RED)entr not found. Install with: apt-get install entr$(NC)"; \
	fi

# Convenience targets for common platforms
esp32: ## Extract and test ESP32 samples only
	$(MAKE) extract-samples-platform PLATFORM=esp32
	$(MAKE) test-samples-platform PLATFORM=esp32

esp8266: ## Extract and test ESP8266 samples only  
	$(MAKE) extract-samples-platform PLATFORM=esp8266
	$(MAKE) test-samples-platform PLATFORM=esp8266

rp2: ## Extract and test RP2 samples only
	$(MAKE) extract-samples-platform PLATFORM=rp2
	$(MAKE) test-samples-platform PLATFORM=rp2

pyboard: ## Extract and test PyBoard samples only
	$(MAKE) extract-samples-platform PLATFORM=pyboard
	$(MAKE) test-samples-platform PLATFORM=pyboard

# Debug and troubleshooting
debug-sample: ## Debug a specific sample file (usage: make debug-sample FILE=sample_001.py)
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)Error: FILE not specified. Usage: make debug-sample FILE=sample_001.py$(NC)"; \
		exit 1; \
	fi
	@if [ -f "$(OUTPUT_PATH)/$(FILE)" ]; then \
		echo "$(BLUE)Debugging sample: $(FILE)$(NC)"; \
		echo "$(YELLOW)File content:$(NC)"; \
		head -20 "$(OUTPUT_PATH)/$(FILE)"; \
		echo ""; \
		echo "$(YELLOW)Running syntax check:$(NC)"; \
		$(PYTHON) -c "import ast; ast.parse(open('$(OUTPUT_PATH)/$(FILE)').read()); print('✓ Syntax OK')"; \
	else \
		echo "$(RED)Sample file not found: $(OUTPUT_PATH)/$(FILE)$(NC)"; \
	fi

version: ## Show version information
	@echo "MicroPython Documentation Sample Testing v0.1.0"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Pytest: $$($(PYTHON) -m pytest --version 2>/dev/null || echo 'Not installed')"
	@echo "MyPy: $$($(PYTHON) -m mypy --version 2>/dev/null || echo 'Not installed')"
	@echo "Docs path: $(DOCS_PATH)"
	@echo "Output path: $(OUTPUT_PATH)"
	@echo "Stubs path: $(MICROPYTHON_STUBS_PATH)"