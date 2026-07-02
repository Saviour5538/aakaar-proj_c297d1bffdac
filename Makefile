# Install dependencies for both backend and frontend
install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

# Start development environment
dev:
	./scripts/dev.sh

# Build the frontend for production
build:
	cd frontend && npm run build

# Start Docker containers
docker-up:
	docker-compose up --build -d

# Stop Docker containers
docker-down:
	docker-compose down

# Clean up Docker containers, volumes, and images
clean:
	docker-compose down -v --rmi all

# Run tests for backend and frontend
test:
	pytest backend/tests
	cd frontend && npm test