# **DudeWheresMyLambo Backend API**

## **Introduction**

Project Delos answers the question: *"If I had bought a crypto currency when it first appeared on the public exchange, would I have enough money to buy a lambo if I sold my coins in the last month?"*

This Flask backend provides cryptocurrency investment analysis with security features, monitoring capabilities, and modern infrastructure support.

---

## **Features**

### **Security**
- Security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)
- Input validation and parameter sanitization
- Configurable rate limiting
- CORS policy management
- Firebase authentication integration

### **Infrastructure**
- SQLite database (lightweight, file-based)
- Docker containerization with multi-stage builds
- Health monitoring and metrics
- Environment-based configuration

### **Testing & Quality**
- Comprehensive test suite (unit and integration tests)
- Test fixtures and mock strategies
- Code quality tools (Black, flake8, mypy, bandit, safety)
- Automated test runner and CI/CD pipeline

### **Documentation**
- OpenAPI 3.0 specification
- Deployment and development guides
- Health monitoring documentation

---

## **Requirements**

### **Core Requirements**
- Python 3.10+
- Docker 20.10+ (for containerized deployment)
- Docker Compose 2.0+ (for local development)

### **Database**
- SQLite (included with Python, no additional setup required)

---

## **🚀 Quick Start**

### **Option 1: Docker Compose (Recommended)**

```bash
# Clone the repository
git clone <repository-url>
cd dwml-backend-flask

# Copy environment configuration
cp env.example .env

# Edit environment variables
nano .env

# Start all services
make docker-run
# or
docker-compose up -d

# Check health
curl http://localhost:8080/health
```

### **Option 2: Local Development**

```bash
# Clone the repository
git clone <repository-url>
cd dwml-backend-flask

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install
# or
pip install -r requirements.txt

# Copy environment configuration
cp env.example .env

# Edit environment variables
nano .env

# Run the application
make dev
# or
python run.py
```

---

## **🔧 Development Setup**

### **1. Environment Configuration**

```bash
# Copy the environment template
cp env.example .env

# Edit the configuration
nano .env
```

**Key Environment Variables:**
```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Database Configuration (SQLite only)
DATABASE_URL=sqlite:///DudeWheresMyLambo.db

# Security Configuration
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
RATE_LIMIT_ENABLED=False
RATE_LIMIT_PER_MINUTE=60

# Feature Flags
ENABLE_NEW_LOGIC=False
ENABLE_CACHING=False  # Disabled - no Redis
ENABLE_MONITORING=True
```

### **2. Development Commands**

```bash
# Install dependencies
make install

# Install development dependencies
make install-dev

# Run development server
make dev

# Run tests
make test

# Run specific test types
make test-unit
make test-integration
make test-e2e

# Code quality
make lint
make format

# Security checks
make security-check

# Clean up
make clean
```

### **3. Database Setup**

```bash
# SQLite database is automatically created when first accessed
# No additional setup required - just run the application
```

---

## **🐳 Docker Deployment**

### **Development with Docker**

```bash
# Build the image
make docker-build

# Run with Docker Compose
make docker-run

# View logs
make docker-logs

# Stop services
make docker-stop
```

### **Production Deployment**

```bash
# Build production image
docker build -t dwml-backend:latest .

# Run with production configuration
docker run -d \
  --name dwml-backend \
  -p 8080:8080 \
  -e FLASK_ENV=production \
  -e DATABASE_URL=sqlite:///DudeWheresMyLambo.db \
  -e SECRET_KEY=your-production-secret \
  dwml-backend:latest
```

### **Docker Compose Production**

```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# With custom environment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## **📊 API Endpoints**

### **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/project/core/process_request` | GET | Process crypto investment analysis |
| `/api/v1/project/core/process_request_grpc` | GET | Process via gRPC |
| `/api/v1/project/core/restricted` | GET | Authentication test |
| `/status` | GET | API status |
| `/` | GET | Welcome message |
| `/graphql` | POST | GraphQL endpoint |
| `/health` | GET | Health check |
| `/metrics` | GET | Application metrics |

### **API Usage Examples**

```bash
# Basic crypto analysis
curl "http://localhost:8080/api/v1/project/core/process_request?symbol=BTC&investment=1000"

# Health check
curl http://localhost:8080/health

# Metrics
curl http://localhost:8080/metrics

# Status
curl http://localhost:8080/status
```

---

## **🧪 Testing**

### **Run All Tests**

```bash
# Run complete test suite
make test

# Run with coverage
make test-coverage

# Run specific test types
make test-unit
make test-integration
make test-e2e

# Backwards compatibility tests
make test-compatibility

# Performance tests
make test-performance
```

### **Test Categories**

- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Contract Tests**: Backwards compatibility verification
- **E2E Tests**: End-to-end workflow testing
- **Performance Tests**: Load and stress testing

### **Test Results**

```bash
# Example test output
pytest tests/ -v --cov=app --cov-report=html
```

---

## **🔒 Security**

### **Security Features**

- **Security Headers**: Automatically added to all responses
- **Input Validation**: Comprehensive parameter validation
- **Rate Limiting**: Configurable rate limiting
- **CORS Protection**: Configurable CORS policies
- **Authentication**: Firebase authentication support
- **Docker Security**: Non-root user, minimal attack surface

### **Security Configuration**

```bash
# Enable rate limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60

# Configure CORS
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Security headers (automatically applied)
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

---

## **📈 Monitoring & Observability**

### **Health Checks**

```bash
# Application health
curl http://localhost:8080/health

# Response example
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "database": "connected",
  "redis": "connected"
}
```

### **Metrics**

```bash
# Application metrics
curl http://localhost:8080/metrics

# Response example
{
  "requests_total": 1250,
  "response_time_avg": 45.2,
  "error_rate": 0.02,
  "active_connections": 12
}
```

### **Logging**

- **Structured Logging**: JSON format for production
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Log Rotation**: Automatic log rotation and cleanup
- **Request Logging**: Comprehensive request/response logging

---

## **🏗️ Architecture**

### **Application Structure**

```
dwml-backend-flask/
├── app/
│   ├── endpoints/              # API endpoints
│   ├── services/               # Business logic
│   ├── models/                 # Data models
│   ├── schemas/                # Validation schemas
│   ├── utils/                  # Utility functions
│   └── middleware/             # Security & rate limiting
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── fixtures/               # Test data
├── docs/                       # Documentation
└── scripts/                    # Deployment scripts
```

### **Database Architecture**

- **Database**: SQLite (lightweight, file-based)
- **Benefits**: No external dependencies, easy deployment, portable

---

## **🚀 Production Deployment**

### **Prerequisites**

- Docker 20.10+
- Docker Compose 2.0+
- SQLite (included with Python)

### **Deployment Steps**

1. **Environment Setup**
   ```bash
   cp env.example .env
   # Edit production configuration
   nano .env
   ```

2. **Database Setup**
   ```bash
   # SQLite database is automatically created
   # No additional setup required
   ```

3. **Deploy with Docker**
   ```bash
   docker-compose up -d
   ```

4. **Verify Deployment**
   ```bash
   curl http://localhost:8080/health
   curl http://localhost:8080/status
   ```

### **Production Configuration**

```bash
# Production environment variables
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
DATABASE_URL=sqlite:///DudeWheresMyLambo.db
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT_ENABLED=True
ENABLE_MONITORING=True
```

---

## **Development Workflow**

### **Trunk-Based Development**

This project follows trunk-based development with production deployments only on `prod/v*` tags:

1. **Development Flow**
   - All development happens on `main`/`master` branch
   - Feature branches are merged directly to main
   - No long-lived feature branches

2. **Production Releases**
   - Production deployments only triggered by `prod/vx.x.x` tags
   - All quality checks and tests must pass before deployment
   - Automatic GitHub release creation

3. **Release Process**
   ```bash
   # Run pre-deployment checks
   make pre-deploy

   # Create production release
   ./scripts/create-prod-release.sh 1.0.0
   ```

### **Code Quality**

The project includes automated quality checks:

1. **Linting and Formatting**
   - Code formatting with Black
   - Linting with flake8
   - Import sorting with isort

2. **Type Checking**
   - Static type checking with mypy
   - Type hints throughout the codebase

3. **Security**
   - Security scanning with bandit
   - Dependency vulnerability scanning with safety

### **Testing**

The test suite includes:

1. **Unit Tests** (`tests/unit/`)
   - Service layer testing (`test_crypto_service.py`)
   - Data model testing (`test_models.py`)
   - Validation schema testing (`test_schemas.py`)

2. **Integration Tests** (`tests/integration/`)
   - API endpoint testing (`test_api_endpoints.py`)
   - Frontend integration testing (`test_frontend.py`)

3. **Test Fixtures** (`tests/fixtures/`)
   - Sample data for testing (`sample_data.json`)
   - Mock objects and test configurations

### **Available Commands**

```bash
# Install dependencies
make install

# Run tests
make test
# Or use the test runner
python3 run_tests.py

# Run specific test categories
python3 -m pytest tests/unit/ -v
python3 -m pytest tests/integration/ -v

# Code formatting
make format

# Linting and type checking
make lint

# Pre-commit hooks (Python equivalent of Husky)
make pre-commit-install  # Install pre-commit hooks
make pre-commit-run      # Run hooks on all files
make pre-commit-update   # Update hooks to latest versions

# Security scanning
make security-check

# Build Docker image
make docker-build

# Run with Docker Compose
make docker-run

# Pre-deployment checks (run before creating prod/v* tag)
make pre-deploy

# Create production release
./scripts/create-prod-release.sh 1.0.0
```

---

## **Documentation**

### **API Documentation**

- OpenAPI 3.0 specification (`openapi-3.0.yaml`)
- Interactive API documentation (when enabled)
- Comprehensive test suite with fixtures

### **Project Documentation**

- Deployment guides in `docs/`
- Development setup instructions
- Architecture and design documentation

---

## **Contributing**

### **Development Workflow**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests and quality checks: `make test && make lint`
5. Commit your changes: `git commit -m "Add your feature"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

### **Code Standards**

- Follow PEP 8 style guide
- Maintain test coverage above 90%
- Update documentation for new features
- Follow security best practices

---

## **Support**

### **Getting Help**

- Documentation: Check the `docs/` directory
- Issues: Create an issue on GitHub
- Discussions: Use GitHub Discussions for questions

### **Common Issues**

1. **Database Connection Issues**
   - Check database configuration: `echo $DATABASE_URL`
   - Verify database service is running: `docker-compose ps`

2. **Docker Issues**
   - Check container status: `docker-compose ps`
   - View application logs: `docker-compose logs flask-app`

3. **Environment Issues**
   - Check environment variables: `cat .env`
   - Verify configuration: `python3 -c "from app.config import get_config; print(get_config())"`

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
