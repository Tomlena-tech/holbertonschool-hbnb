# Makefile for running unit tests in the test_models folder

# Colors for pretty output
GREEN := \033[1;32m
RED := \033[1;31m
YELLOW := \033[1;33m
NC := \033[0m  # No Color

# Default target
.PHONY: test
test:
	@echo "$(YELLOW)🔍 Running all unittests in test_models...$(NC)"
	@python3 -m unittest discover -s test_models -p "test_*.py" -v || \
		(echo "$(RED)❌ Some tests failed.$(NC)" && exit 1)
	@echo "$(GREEN)✅ All tests completed.$(NC)"

# Run a single test file (usage: make single file=test_models/test_base_model.py)
.PHONY: single
single:
	@if [ -z "$(file)" ]; then \
		echo "$(RED)❌ Usage: make single file=test_models/test_base_model.py$(NC)"; \
	else \
		echo "$(YELLOW)🧪 Running single test: $(file)...$(NC)"; \
		python3 -m unittest $(file) -v || \
			(echo "$(RED)❌ Test failed.$(NC)" && exit 1); \
		echo "$(GREEN)✅ Test passed.$(NC)"; \
	fi

# Clean up Python cache and compiled files
.PHONY: clean
clean:
	@echo "$(YELLOW)🧹 Cleaning up __pycache__ and .pyc files...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✅ Cleanup complete.$(NC)"

# Optional: help target to list commands
.PHONY: help
help:
	@echo "$(YELLOW)Available commands:$(NC)"
	@echo "  make test          - Run all test files in test_models/"
	@echo "  make single file=... - Run a single test file (e.g. make single file=test_models/test_base_model.py)"
	@echo "  make clean         - Remove Python cache files"
	@echo "  make help          - Show this help message"