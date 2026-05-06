# Network Security Phishing Detection System

This project is an end-to-end machine learning system for phishing website detection. It includes data ingestion, validation, transformation, model training, experiment tracking, API deployment, Dockerization, and CI/CD deployment on AWS.

The system allows users to upload website-related feature data and receive phishing predictions through a FastAPI application.

---

# Project Overview

The project is designed to simulate a production-grade machine learning workflow with modular architecture and deployment automation.

The pipeline includes:

* Data ingestion from MongoDB
* Data validation and schema checks
* Data transformation using preprocessing pipelines
* Model training and evaluation
* MLflow experiment tracking with DagsHub integration
* FastAPI inference API
* Docker containerization
* CI/CD using GitHub Actions
* AWS EC2 deployment with Amazon ECR

---

# Tech Stack

## Backend

* Python
* FastAPI
* Uvicorn

## Machine Learning

* Scikit-learn
* Pandas
* NumPy

## Experiment Tracking

* MLflow
* DagsHub

## Database

* MongoDB Atlas

## Deployment & DevOps

* Docker
* GitHub Actions
* Amazon ECR
* AWS EC2

---

# Project Structure

```text
networksecurity/
│
├── networksecurity/
│   ├── components/
│   ├── pipeline/
│   ├── entity/
│   ├── constants/
│   ├── utils/
│   ├── logging/
│   └── exception/
│
├── templates/
├── valid_data/
├── data_schema/
├── final_model/
├── logs/
│
├── app.py
├── main.py
├── push_data.py
├── requirements.txt
├── setup.py
├── Dockerfile
└── README.md
```

---

# Features

* Modular ML pipeline architecture
* Automated data validation
* Model training and evaluation
* Experiment tracking using MLflow
* Prediction API using FastAPI
* CSV upload prediction support
* Dockerized deployment
* CI/CD pipeline with GitHub Actions
* AWS deployment using EC2 and ECR

---

# Dataset

The dataset contains engineered website-related features used for phishing detection.

Example features include:

* URL length
* HTTPS token
* SSL final state
* Having IP address
* Request URL
* Web traffic
* Google index
* Domain registration length

The target variable indicates whether a website is phishing or legitimate.

---

# Installation

## Clone the repository

```bash
git clone https://github.com/abhikdas98/networksecurity.git
```

```bash
cd networksecurity
```

---

# Create virtual environment

```bash
python -m venv venv
```

## Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

# Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory.

```env
MONGODB_URL_KEY=your_mongodb_connection_string
```

---

# Run Training Pipeline

```bash
python main.py
```

This will:

* ingest data
* validate schema
* transform data
* train models
* save trained artifacts
* track experiments in MLflow

---

# Run FastAPI Application

```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

Application endpoints:

| Endpoint   | Description                    |
| ---------- | ------------------------------ |
| `/docs`    | Swagger UI                     |
| `/train`   | Trigger training pipeline      |
| `/predict` | Upload CSV and get predictions |

---

# Docker Setup

## Build Docker image

```bash
docker build -t networksecurity .
```

## Run container

```bash
docker run -d -p 8080:8080 networksecurity
```

---

# MLflow Tracking

MLflow is integrated with DagsHub for experiment tracking.

Tracked items include:

* model parameters
* evaluation metrics
* trained models
* experiment runs

---

# CI/CD Pipeline

The project uses GitHub Actions for:

* Continuous Integration
* Docker image build
* Amazon ECR push
* EC2 deployment

Deployment flow:

```text
GitHub Push
    ↓
GitHub Actions
    ↓
Docker Build
    ↓
Push to Amazon ECR
    ↓
EC2 Pulls Latest Image
    ↓
Container Deployment
```

---

# AWS Deployment

Deployment is performed using:

* Amazon EC2
* Amazon ECR
* Self-hosted GitHub Actions runner

The FastAPI application is exposed publicly through EC2.

---

# Future Improvements

* Model versioning
* Monitoring and logging dashboard
* Nginx reverse proxy
* HTTPS support
* Kubernetes deployment
* Automated retraining pipeline
* Separate training and inference services

---

# Author

Abhik Das

GitHub:
[text](https://github.com/abhikdas98)