<div align="center">

<img src="https://www.edwinkassier.com/Assets/Monogram.png" alt="Ashes Project Monogram" width="80" height="80">

# Ashes Project Flask API Boilerplate

<div align="center">

**A Flask API boilerplate for rapid development**

</div>

<div align="center">

[![codecov](https://codecov.io/gh/YOUR_USERNAME/flask-api-boilerplate/branch/master/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/flask-api-boilerplate)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask 2.2+](https://img.shields.io/badge/flask-2.2+-green.svg)](https://flask.palletsprojects.com/)

</div>

<div align="center">

[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

</div>

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [Installation Options](#installation-options)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Security](#security)
- [CI/CD Pipeline](#cicd-pipeline)
- [Available Commands](#available-commands)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

A Flask API boilerplate designed for rapid development of web APIs.

This template provides everything you need to build scalable, maintainable web APIs with Flask. It includes features like automated testing, CI/CD pipelines, security scanning, monitoring, and deployment automation.

### API Architecture

The boilerplate supports both **REST** and **GraphQL** endpoints, giving you flexibility in how you build your API:

- **REST API**: Traditional HTTP endpoints with JSON responses
- **GraphQL**: Flexible query language for efficient data fetching
- **OpenAPI Documentation**: Interactive API documentation for both interfaces

### Feature Overview

| **Development** | **Testing** | **Deployment** |
|:---|:---|:---|
| Pre-commit hooks | Unit tests | Docker containers |
| Code formatting | Integration tests | CI/CD pipeline |
| Type checking | Coverage reporting | Cloud deployment |
| Linting | Test automation | Health monitoring |

---

## Key Features

| **Architecture** | **Security** | **Monitoring** | **Performance** |
|:---|:---|:---|:---|
| Domain-Driven Design | Security Scanning | Health Checks | SQLite Database |
| Rich Domain Models | Dependency Checks | Structured Logging | Docker Optimization |
| Clean Separation | Authentication | Error Tracking | API Rate Limiting |

### Feature Categories

<details>
<summary><b>🔒 Security Features</b></summary>

- ✅ **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection
- ✅ **Input Validation**: Comprehensive parameter sanitization
- ✅ **Rate Limiting**: Configurable rate limiting
- ✅ **CORS Protection**: Configurable CORS policies
- ✅ **Authentication**: Firebase authentication integration

</details>

<details>
<summary><b>🏗️ Architecture</b></summary>

- ✅ **Domain-Driven Design**: Two-domain architecture (domain + shared)
- ✅ **Rich Domain Models**: Business logic encapsulated in models
- ✅ **Service Layer**: Orchestration and business workflows
- ✅ **Central Router**: Single registration point for all domains
- ✅ **Clean Separation**: Clear boundaries between layers

</details>

<details>
<summary><b>🔧 Infrastructure</b></summary>

- ✅ **Database**: SQLite (lightweight, file-based)
- ✅ **Containerization**: Multi-stage Docker builds
- ✅ **Health Monitoring**: Application health checks
- ✅ **Configuration**: Environment-based configuration
- ✅ **Deployment**: Docker Compose support

</details>

<details>
<summary><b>🧪 Testing & Quality</b></summary>

- ✅ **Testing**: Comprehensive test suite (unit and integration)
- ✅ **Coverage**: Automated coverage reporting
- ✅ **Quality Tools**: Black, flake8, mypy, bandit, safety
- ✅ **CI/CD**: Automated test runner and pipeline
- ✅ **Fixtures**: Test fixtures and mock strategies

</details>

<details>
<summary><b>📚 Documentation</b></summary>

- ✅ **API Docs**: OpenAPI 3.0 specification
- ✅ **Deployment**: Comprehensive deployment guides
- ✅ **Development**: Setup and development guides
- ✅ **Monitoring**: Health monitoring documentation

</details>

---

## System Architecture

### Application Structure

```
dwml-backend-flask/
├── app/                      # Flask application
│   ├── domain/              # Main DWML application domain (complete)
│   │   ├── models.py        # Domain models (Investment, PriceData)
│   │   ├── services.py      # Business logic (CryptoAnalysisService)
│   │   ├── routes.py        # HTTP endpoints (REST API)
│   │   ├── schemas.py       # Validation schemas (Marshmallow)
│   │   ├── graphql_schema.py # GraphQL API schema
│   │   ├── proto_files/     # gRPC protocol buffers
│   │   ├── exceptions.py    # Domain-specific exceptions
│   │   └── constants.py     # Domain constants
│   ├── shared/              # Shared infrastructure
│   │   └── middleware/      # Cross-cutting concerns
│   │       ├── auth.py      # Firebase authentication
│   │       ├── cors.py      # CORS configuration
│   │       ├── error_handler.py # Centralized error handling
│   │       ├── rate_limit.py # Rate limiting
│   │       └── security.py  # Security headers
│   ├── router.py            # Central route registration
│   ├── config.py            # Configuration management
│   └── extensions.py        # Flask extensions (SQLAlchemy)
├── tests/                   # Test suites
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── docs/                    # Documentation
├── scripts/                 # Deployment scripts
├── .github/workflows/       # CI/CD pipelines
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Docker Compose
└── Makefile               # Development commands
```

### Architecture Principles

This project follows a **clean domain-driven architecture**:

#### 🎯 **`domain/`** - Complete DWML Application Domain
The domain owns its **entire vertical slice**:
- **Business Logic**: Rich domain models with business rules
- **REST API**: HTTP endpoints via Flask blueprints
- **GraphQL API**: Flexible query interface
- **gRPC API**: Protocol buffer definitions
- **Validation**: Request/response schemas
- **Error Handling**: Domain-specific exceptions
- **Configuration**: Domain constants

#### 🔧 **`shared/`** - Shared Infrastructure
Cross-cutting concerns used by all domains:
- **Middleware**: Authentication, CORS, rate limiting, security
- *(Future)* Common utilities, helpers, reusable components

### Database Architecture

- **Database**: SQLite (lightweight, file-based)
- **Benefits**: No external dependencies, easy deployment, portable

---

## Quick Start

### Get up and running in 5 minutes!

### Prerequisites

- **Python 3.10+**
- **pip or Pipenv**
- **Git**
- **Docker (optional)**

### Step-by-Step Setup

<details>
<summary><b>1. Clone the Repository</b></summary>

```bash
# Clone the repository
git clone <repository-url>
cd flask-api-boilerplate

# Navigate to project directory
cd flask-api-boilerplate
```

</details>

<details>
<summary><b>2. Set Up Development Environment</b></summary>

```bash
# Install dependencies and setup pre-commit hooks
make install-dev

# This will:
# ✅ Install all Python dependencies
# ✅ Set up pre-commit hooks
# ✅ Configure development tools
# ✅ Set up code quality tools
```

</details>

<details>
<summary><b>3. Configure Environment</b></summary>

```bash
# Copy environment template
cp env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///DudeWheresMyLambo.db
```

</details>

<details>
<summary><b>4. Start Development Server</b></summary>

```bash
# Start the development server
make dev

# The API will be available at:
# http://localhost:8080
# Health Check: http://localhost:8080/health
# Status: http://localhost:8080/status
```

</details>

---

## Installation Options

### Choose your preferred installation method

| **Make Commands** | **Docker Compose** | **Manual Installation** |
|:---|:---|:---|
| *Recommended* | *Containerized* | *Custom setup* |
| ```bash<br/>make install-dev<br/>``` | ```bash<br/>docker-compose up -d<br/>``` | ```bash<br/>pip install -r requirements.txt<br/>``` |
| ✅ Easy setup | ✅ Isolated environment | ✅ Full control |
| ✅ Automated configuration | ✅ Easy cleanup | ✅ Custom configuration |
| ✅ Pre-commit hooks | ✅ Production-like setup | ✅ Custom configuration |

### Docker Installation

<details>
<summary><b>Using Docker Compose (Recommended)</b></summary>

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f flask-app

# Stop services
docker-compose down
```

**Services included:**
- Web application (Flask)
- Database (SQLite)
- Monitoring (Health checks)

</details>

---

## Testing

### Testing Suite

| **Unit Tests** | **Integration Tests** | **Coverage Report** | **All Tests** |
|:---|:---|:---|:---|
| *Fast & Isolated* | *API & Database* | *Code Coverage* | *Complete Suite* |
| ```bash<br/>make test-unit<br/>``` | ```bash<br/>make test-integration<br/>``` | ```bash<br/>make test-coverage<br/>``` | ```bash<br/>make test<br/>``` |
| ✅ Model tests | ✅ API endpoint tests | ✅ Coverage metrics | ✅ Unit + Integration |
| ✅ Service tests | ✅ Database integration | ✅ HTML reports | ✅ Coverage reporting |
| ✅ Utility tests | ✅ External service tests | ✅ Coverage goals | ✅ Performance tests |

### Coverage Goals

| Component | Target | Current |
|:---|:---|:---|
| **Overall** | 80%+ | ✅ |
| **Critical Modules** | 90%+ | ✅ |
| **New Code** | 90%+ | ✅ |

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Contract Tests**: Backwards compatibility verification
- **E2E Tests**: End-to-end workflow testing
- **Performance Tests**: Load and stress testing

---

## Code Quality

### Automated Code Quality Tools

| **Black** | **Flake8** | **isort** | **Mypy** | **Pre-commit** |
|:---|:---|:---|:---|:---|
| *Code Formatting* | *Linting* | *Import Sorting* | *Type Checking* | *Automated Hooks* |
| ```bash<br/>make format<br/>``` | ```bash<br/>make lint<br/>``` | ```bash<br/>make format<br/>``` | ```bash<br/>make lint<br/>``` | ```bash<br/>pre-commit install<br/>``` |
| ✅ Consistent formatting | ✅ Style guide compliance | ✅ Import organization | ✅ Type safety | ✅ Git hooks |
| ✅ Line length: 88 | ✅ Error detection | ✅ Group sorting | ✅ Static analysis | ✅ Auto-checks |
| ✅ Auto-formatting | ✅ Best practices | ✅ Auto-sorting | ✅ Error prevention | ✅ Quality gates |

---

## Security

### Security Measures

| **Bandit** | **Safety** | **Authentication** |
|:---|:---|:---|
| *Security Analysis* | *Dependency Scanning* | *Access Control* |
| ```bash<br/>make security-check<br/>``` | ```bash<br/>make security-check<br/>``` | ```bash<br/># Firebase, API Key, Session<br/>``` |
| ✅ Security vulnerabilities | ✅ Known vulnerabilities | ✅ Multiple auth methods |
| ✅ Best practices | ✅ Dependency updates | ✅ Role-based access |
| ✅ Risk assessment | ✅ Security patches | ✅ Token management |

### Security Configuration

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

## CI/CD Pipeline

### Automated Deployment Pipeline

### Pipeline Stages

| **Quality Checks** | **Testing** | **Security** | **Deployment** |
|:---|:---|:---|:---|
| *Code Quality* | *Test Suite* | *Security Scanning* | *Production Release* |
| - Black formatting | - Unit tests | - Bandit security scan | - Docker build |
| - Flake8 linting | - Integration tests | - Safety dependency check | - Registry push |
| - Mypy type checking | - Coverage reporting | - Vulnerability assessment | - Cloud deployment |
| - isort import sorting | - Performance tests | - Security best practices | - Health verification |

### Pipeline Triggers

| **Branch Push** | **Pull Request** | **Tag Release** |
|:---|:---|:---|
| *Development* | *Code Review* | *Production* |
| ```bash<br/>git push origin main<br/>``` | ```bash<br/># Create PR to main<br/>``` | ```bash<br/>git tag prod/v1.0.0<br/>git push origin prod/v1.0.0<br/>``` |
| ✅ Quality checks | ✅ Quality checks | ✅ Full pipeline |
| ✅ Testing | ✅ Testing | ✅ Production deployment |
| ✅ Security scans | ✅ Security scans | ✅ Health verification |
| | ✅ Code review | ✅ Release creation |

---

## Available Commands

### Development Commands

| **Installation** | **Testing** | **Code Quality** |
|:---|:---|:---|
| ```bash<br/>make install<br/>make install-dev<br/>``` | ```bash<br/>make test<br/>make test-unit<br/>make test-integration<br/>make test-coverage<br/>``` | ```bash<br/>make format<br/>make lint<br/>make security-check<br/>``` |
| **Development** | **Database** | **Docker** |
| ```bash<br/>make dev<br/>make prod<br/>make clean<br/>make pre-deploy<br/>``` | ```bash<br/>make db-init<br/>make db-migrate<br/>``` | ```bash<br/>make docker-build<br/>make docker-run<br/>make docker-stop<br/>make docker-logs<br/>``` |
| **Utilities** | **Pre-commit** | **CI/CD** |
| ```bash<br/>make help<br/>make validate-requirements<br/>make docs<br/>``` | ```bash<br/>make pre-commit-install<br/>make pre-commit-run<br/>make pre-commit-update<br/>``` | ```bash<br/>make ci<br/>make create-prod-tag<br/>``` |

---

## Deployment

### Production Deployment Guide

### Tag-Based Deployment

| **Create Release** | **Version Format** |
|:---|:---|
| ```bash<br/># Using release script<br/>./scripts/create-prod-release.sh 1.0.0<br/><br/># Or manually<br/>git tag -a prod/v1.0.0 -m "Release v1.0.0"<br/>git push origin prod/v1.0.0<br/>``` | ```bash<br/>prod/vMAJOR.MINOR.PATCH<br/><br/># Examples:<br/>prod/v1.0.0<br/>prod/v1.2.3<br/>prod/v2.0.0<br/>``` |

### Production Configuration

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

## Monitoring

### Production Monitoring

| **Health Checks** | **Status** | **Logging** |
|:---|:---|:---|
| *System Status* | *Service Info* | *Structured Logs* |
| ```bash<br/>GET /health<br/>``` | ```bash<br/>GET /status<br/>``` | ```bash<br/># Python logging<br/>``` |
| ✅ Application health | ✅ API version | ✅ Request logging |
| ✅ Service status | ✅ Service name | ✅ Error logging |
| ✅ Timestamp | ✅ Running status | ✅ Performance logs |

### Health Check Response

```json
{
  "status": "healthy",
  "service": "dwml-backend",
  "timestamp": "2024-01-01T00:00:00.000000"
}
```

### Status Response

```json
{
  "message": "DudeWheresMyLambo API Status : Running!",
  "version": "1.0.0"
}
```

---

## API Documentation

### Interactive API Documentation

| **Health** | **Status** | **Welcome** | **GraphQL** |
|:---|:---|:---|:---|
| ```bash<br/>GET /health<br/>``` | ```bash<br/>GET /status<br/>``` | ```bash<br/>GET /<br/>``` | ```bash<br/>POST /graphql<br/>``` |

### Main Endpoints

All endpoints are registered through the central router (`app/router.py`):

| **Endpoint** | **Method** | **Description** | **Domain** |
|:---|:---|:---|:---|
| `/api/v1/process_request` | GET | Analyze crypto investment | `domain` |
| `/api/v1/process_request_grpc` | GET | Analyze via gRPC | `domain` |
| `/api/v1/restricted` | GET | Authentication test | `domain` |
| `/health` | GET | Health check | `router` |
| `/status` | GET | API status | `router` |
| `/` | GET | Welcome message | `router` |
| `/graphql` | POST | GraphQL endpoint | `schemas` |

**Request Example:**
```bash
GET /api/v1/process_request?symbol=BTC&investment=1000
```

**Response:**
```json
{
  "message": {
    "SYMBOL": "BTC",
    "INVESTMENT": 1000.0,
    "NUMBERCOINS": 0.05,
    "PROFIT": 250.0,
    "GROWTHFACTOR": 0.25,
    "LAMBOS": 0.00125,
    "GENERATIONDATE": "2024-01-01T00:00:00Z"
  },
  "graph_data": [
    {"x": "2024-01-01 00:00:00", "y": 20000.0},
    {"x": "2024-01-02 00:00:00", "y": 21000.0}
  ]
}
```

### API Usage Examples

```bash
# Analyze crypto investment
curl "http://localhost:8080/api/v1/process_request?symbol=BTC&investment=1000"

# Analyze via gRPC
curl "http://localhost:8080/api/v1/process_request_grpc?symbol=ETH&investment=500"

# Health check
curl http://localhost:8080/health

# Status
curl http://localhost:8080/status

# Welcome message
curl http://localhost:8080/

# Authenticated endpoint (requires Firebase token)
curl -H "Authorization: Bearer <token>" http://localhost:8080/api/v1/restricted
```

### Interacting with the Live System

Once deployed, you can interact with the system through multiple interfaces:

#### REST API
```bash
# Health check
curl https://your-domain.com/health

# API status
curl https://your-domain.com/status

# Analyze crypto investment
curl "https://your-domain.com/api/v1/process_request?symbol=BTC&investment=1000"

# Analyze via gRPC
curl "https://your-domain.com/api/v1/process_request_grpc?symbol=ETH&investment=500"
```

#### GraphQL
```bash
# GraphQL query
curl -X POST https://your-domain.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ processRequest(symbol: \"BTC\", investment: 1000) { message graphData } }"}'
```

---

## Project Structure

### Organized Codebase

```
dwml-backend-flask/
├── app/                      # Flask application
│   ├── domain/              # Main DWML application domain (complete)
│   │   ├── __init__.py      # Domain exports
│   │   ├── models.py        # Domain models (Investment, PriceData)
│   │   ├── services.py      # Business logic (CryptoAnalysisService)
│   │   ├── routes.py        # HTTP endpoints (REST API)
│   │   ├── schemas.py       # Validation schemas (Marshmallow)
│   │   ├── graphql_schema.py # GraphQL API schema
│   │   ├── proto_files/     # gRPC protocol buffers
│   │   │   ├── api.proto    # Protocol definition
│   │   │   ├── api_pb2.py   # Generated Python code
│   │   │   └── api_pb2_grpc.py # gRPC stubs
│   │   ├── exceptions.py    # Domain-specific exceptions
│   │   └── constants.py     # Domain constants (LAMBO_PRICE, etc.)
│   ├── shared/              # Shared infrastructure
│   │   └── middleware/      # Cross-cutting concerns
│   │       ├── __init__.py
│   │       ├── auth.py      # Firebase authentication
│   │       ├── cors.py      # CORS configuration
│   │       ├── error_handler.py # Centralized error handling
│   │       ├── rate_limit.py # Rate limiting
│   │       └── security.py  # Security headers
│   ├── router.py            # Central route registration
│   ├── config.py            # Configuration management
│   ├── extensions.py        # Flask extensions (SQLAlchemy, etc.)
│   └── __init__.py         # Application factory
├── tests/                   # Test suites
│   ├── unit/               # Unit tests (models, services, schemas)
│   ├── integration/        # Integration tests (API endpoints)
│   ├── fixtures/           # Test fixtures and data
│   └── conftest.py         # Pytest configuration
├── docs/                    # Documentation
│   ├── Architecture.png    # Architecture diagram
│   └── BuildPipeline.png   # CI/CD pipeline diagram
├── scripts/                 # Utility scripts
│   ├── create-prod-release.sh    # Production release script
│   └── setup-pre-commit.sh       # Pre-commit setup
├── .github/workflows/       # CI/CD pipelines
│   └── push.yml            # GitHub Actions workflow
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Docker Compose setup
├── Makefile               # Development commands
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Python project config
└── README.md              # This file
```

### Clean Domain-Driven Architecture

**Perfect Domain Ownership:**

Each domain owns its **entire vertical slice**:

#### 🎯 `app/domain/` - DWML Application
- **Business Logic**: `models.py`, `services.py`
- **API Interfaces**: `routes.py` (REST), `graphql_schema.py` (GraphQL), `proto_files/` (gRPC)
- **Validation**: `schemas.py` (Marshmallow)
- **Error Handling**: `exceptions.py`
- **Configuration**: `constants.py`

#### 🔧 `app/shared/` - Shared Infrastructure
- **Middleware**: Authentication, CORS, rate limiting, security headers
- *(Add shared utilities as needed)*

**Key Benefits:**
- ✅ Complete domain ownership (100% vertical slice)
- ✅ Zero scattered code across folders
- ✅ Clear separation of concerns
- ✅ Easy to test, maintain, and scale
- ✅ Simple to add new domains
- ✅ True Domain-Driven Design

---

## Contributing

### How to Contribute

| **1. Fork & Clone** | **2. Create Branch** | **3. Make Changes** | **4. Submit PR** |
|:---|:---|:---|:---|
| ```bash<br/>git clone <your-fork><br/>cd flask-api-boilerplate<br/>``` | ```bash<br/>git checkout -b feature/your-feature<br/>``` | ```bash<br/># Make your changes<br/>make format<br/>make lint<br/>make test<br/>``` | ```bash<br/>git push origin feature/your-feature<br/># Create pull request<br/>``` |

### Code Standards

| **Style** | **Types** | **Testing** | **Documentation** |
|:---|:---|:---|:---|
| - PEP 8 compliance | - Type hints required | - Write tests | - Docstrings |
| - Black formatting | - Mypy compliance | - 80%+ coverage | - README updates |
| - 88 character limit | - Static analysis | - Test documentation | - Code comments |

---

## Troubleshooting

### Common Issues & Solutions

<details>
<summary><b>Pre-commit Hooks Failing</b></summary>

```bash
# Update pre-commit hooks
pre-commit autoupdate

# Run manually to see errors
pre-commit run --all-files

# Skip hooks temporarily
git commit --no-verify -m "message"
```

</details>

<details>
<summary><b>Tests Failing</b></summary>

```bash
# Run with verbose output
pytest -vv --tb=long

# Run specific test
pytest tests/unit/test_models.py::TestResultsModel::test_create_result -v

# Run with coverage
pytest --cov=app --cov-report=html
```

</details>

<details>
<summary><b>Docker Issues</b></summary>

```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs -f flask-app

# Clean up
docker-compose down -v
docker system prune -a
```

</details>

<details>
<summary><b>Import Errors</b></summary>

```bash
# Check Python version
python --version  # Should be 3.10+

# Check installed packages
pip list

# Reinstall dependencies
make clean
make install-dev

# Check virtual environment
which python
which pip
```

</details>

<details>
<summary><b>Database Connection Issues</b></summary>

```bash
# Check database configuration
echo $DATABASE_URL

# Verify database service is running
docker-compose ps

# Check SQLite database
ls -la *.db
```

</details>

<details>
<summary><b>Environment Issues</b></summary>

```bash
# Check environment variables
cat .env

# Verify configuration
python3 -c "from app.config import get_config; print(get_config())"

# Check Flask environment
echo $FLASK_ENV
```

</details>

---

## License

### MIT License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
