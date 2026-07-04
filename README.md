# 🚀 Flask-CI-CD-Pipeline: Automated DevOps Architecture

[![Jenkins Pipeline](https://img.shields.io/badge/Jenkins-Declarative%20Pipeline-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Python Flask](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://flask.palletprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **Hero Vired DevOps Assignment Submission**  
> **Student Name**: Kaushal Patil  
> **Hero Vired ID**: KaushalPatil_13408  
> **Email ID**: patilkaushal89@gmail.com  
> **Repository URL**: [https://github.com/kaushalpatil205/Flask-CI-CD-Pipeline](https://github.com/kaushalpatil205/Flask-CI-CD-Pipeline)

---

## 📑 Table of Contents
1. [Project Overview & Objective](#-project-overview--objective)
2. [Architectural Workflow Diagram](#-architectural-workflow-diagram)
3. [Part 1: Jenkins CI/CD Pipeline Implementation](#-part-1-jenkins-cicd-pipeline-implementation)
   - [Jenkins Docker Setup & Prerequisites](#1-jenkins-docker-setup--prerequisites)
   - [Jenkinsfile Declarative Stages](#2-jenkinsfile-declarative-stages)
   - [Jenkins Execution Proofs & Screenshots](#3-jenkins-execution-proofs--screenshots)
4. [Part 2: GitHub Actions CI/CD Implementation](#-part-2-github-actions-cicd-implementation)
   - [Workflow Triggers & Jobs](#1-workflow-triggers--jobs)
   - [Environment Secrets & Security](#2-environment-secrets--security)
   - [GitHub Actions Execution Proofs & Screenshots](#3-github-actions-execution-proofs--screenshots)
5. [Local Verification & Testing](#-local-verification--testing)
6. [Conclusion & DevOps Best Practices](#-conclusion--devops-best-practices)

---

## 🎯 Project Overview & Objective

In modern software engineering, Continuous Integration (CI) and Continuous Deployment (CD) are vital for maintaining code quality, accelerating release cycles, and minimizing human error during deployments. 

This repository implements a production-grade, end-to-end CI/CD automation suite for a **Python Flask Web Application** (Student Registration System with MongoDB backend). The assignment demonstrates mastery of two industry-leading automation platforms:
1. **Self-Hosted Enterprise CI/CD**: Using **Jenkins** running in a containerized Docker environment, utilizing a declarative `Jenkinsfile` for building, testing, and simulating deployments.
2. **Cloud-Native CI/CD**: Using **GitHub Actions**, leveraging multi-stage YAML workflows triggered by branch pushes and GitHub release tags, complete with encrypted environment secrets.

---

## 🏛️ Architectural Workflow Diagram

```
===================================================================================================
                                  AUTOMATED DEVOPS CI/CD PIPELINE
===================================================================================================

       [ Developer Pushes Code to GitHub / Creates Release Tag ]
                                  │
          ┌───────────────────────┴───────────────────────┐
          ▼                                               ▼
┌───────────────────────────────────┐   ┌───────────────────────────────────┐
│        JENKINS CI/CD SERVER       │   │        GITHUB ACTIONS CI/CD       │
│  (Self-Hosted via Docker Engine)  │   │     (Cloud-Native Runner VMs)     │
└───────────────────────────────────┘   └───────────────────────────────────┘
          │                                               │
          ├─► 1. Poll SCM (H/5 * * * *)                   ├─► 1. Event Trigger Evaluation
          │                                               │      ├── push: [ main, staging ]
          ├─► 2. Build Stage                              │      └── release: [ created ]
          │      ├── Create Python Virtual Env            │
          │      └── pip install -r requirements.txt      ├─► 2. Job: build-and-test
          │                                               │      ├── Setup Python 3.10 Environment
          ├─► 3. Test Stage                               │      ├── Install Pip Dependencies
          │      └── pytest --maxfail=1 -q                │      └── Execute Unit Test Suite
          │                                               │
          ├─► 4. Deploy Stage (Branch: main)              ├─► 3. Job: build (Artifact Packaging)
          │      └── Simulate Staging Server Deploy       │      └── Upload flask-app-package
          │                                               │
          └─► 5. Post Actions                             ├─► 4. Job: deploy-staging
                 ├── Success Notification                 │      ├── Condition: push to `staging`
                 └── Failure Alert / Log Dump             │      └── Simulate Staging Server Deploy
                                                          │
                                                          └─► 5. Job: deploy-production
                                                                 ├── Condition: tag release `v*`
                                                                 └── Simulate Production Deploy
===================================================================================================
```

---

## 🛠️ Part 1: Jenkins CI/CD Pipeline Implementation

The Jenkins automation pipeline is scripted using Jenkins Declarative syntax within the root `Jenkinsfile`. It ensures that every code change is isolated in a virtual environment, dependencies are upgraded, unit tests are executed, and builds are validated before deployment.

### 1. Jenkins Docker Setup & Prerequisites
To avoid local Java/OS dependency conflicts, Jenkins was hosted inside a clean Docker container on macOS with port mappings for web UI and agent communication.

#### Step A: Launch Jenkins Container
```bash
docker run -d \
  --name jenkins-server \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

#### Step B: Equip Container with Python 3 & venv
Because the default Jenkins LTS image includes only Java runtime environments, Python 3 and virtual environment capabilities were injected into the running container as root:
```bash
docker exec -u 0 -it jenkins-server bash -c "apt-get update && apt-get install -y python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*"
```

#### Step C: Pipeline Configuration in Jenkins Dashboard
1. Created a new **Pipeline Item** named `Flask-CI-CD-Pipeline`.
2. Configured **Build Triggers** to use **Poll SCM** with the schedule `H/5 * * * *` (polling GitHub every 5 minutes for new commits).
3. Set **Pipeline Definition** to `Pipeline script from SCM`.
4. Connected the **Git Repository URL**: `https://github.com/kaushalpatil205/Flask-CI-CD-Pipeline.git` targeting branch `*/main` and script path `Jenkinsfile`.

---

### 2. Jenkinsfile Declarative Stages

The pipeline consists of three sequential stages and robust post-action handlers:
- **Build: Install Dependencies**: Creates a fresh virtual environment (`venv`), upgrades `pip`, and installs all backend packages required by `requirements.txt` (Flask, PyMongo, python-dotenv, pytest).
- **Test: Run Unit Tests**: Activates the virtual environment and executes `pytest --maxfail=1 --disable-warnings -q` against the automated test suite in `test_app.py`.
- **Deploy: Staging Environment**: Conditioned to execute only when building the `main` branch. Simulates a live deployment to the staging server and logs deployment timestamps.
- **Post Actions**: Automatically outputs colored log metrics and status notifications upon pipeline completion or failure.

---

### 3. Jenkins Execution Proofs & Screenshots

The following visual checkpoints confirm the successful configuration and execution of the Jenkins pipeline:

#### 📸 1. Jenkins Pipeline Configuration & SCM Setup
*Shows the Git repository URL connection, branch specifier (`*/main`), and polling automation.*
![Jenkins Configuration](screenshots/01_jenkins_pipeline_config.png)

#### 📸 2. Jenkins Stage View (Build, Test, Deploy Success)
*Shows the visual pipeline grid with all stages (Build, Test, Deploy) passing successfully in green.*
![Jenkins Stage View](screenshots/02_jenkins_stage_view.png)

#### 📸 3. Jenkins Console Output & Unit Test Validation
*Shows the raw console logs verifying virtual environment creation, successful installation of dependencies, and `3 passed` pytest results.*
![Jenkins Console Output](screenshots/03_jenkins_console_output.png)

---

## 🐙 Part 2: GitHub Actions CI/CD Implementation

For cloud-native CI/CD without server management, a comprehensive multi-job YAML workflow was engineered in `.github/workflows/ci-cd.yml`. This workflow leverages GitHub-hosted Ubuntu runners (`ubuntu-latest`) to automate verification across multiple environment tiers.

### 1. Workflow Triggers & Jobs

The GitHub Actions workflow is engineered to respond to specific Git lifecycle events:

| Job Name | Trigger Condition | Execution Actions & Purpose |
| :--- | :--- | :--- |
| **`build-and-test`** | Pushes to `main` or `staging`, or Release creation | Checks out source code, initializes Python 3.10 with pip caching, installs dependencies, and runs `pytest`. |
| **`build`** | Successful completion of `build-and-test` | Packages source files and dependencies into an artifact folder (`build_output`) and uploads it as `flask-app-package`. |
| **`deploy-staging`** | Push event occurring specifically on branch `staging` | Downloads build artifacts, injects encrypted environment secrets, and deploys to the Staging server. |
| **`deploy-production`** | Creation of a formal GitHub Release tag (e.g., `v1.0.0`) | Downloads build artifacts, authenticates with secure deployment keys, and deploys the live update to Production. |

---

### 2. Environment Secrets & Security

In compliance with enterprise DevOps security guidelines, sensitive deployment credentials and API tokens are never hardcoded in source code. They are encrypted and stored inside GitHub Repository Settings under **Settings > Secrets and variables > Actions**:
- `DEPLOY_KEY`: SSH private RSA key used for secure server-to-server deployment authentication.
- `API_TOKEN`: Encrypted API authorization token required for third-party cloud service integrations.

During deployment stages, these secrets are securely exposed as environment variables (`${{ secrets.API_TOKEN }}` and `${{ secrets.DEPLOY_KEY }}`).

---

### 3. GitHub Actions Execution Proofs & Screenshots

The following screenshots validate the GitHub Actions workflow execution across staging and production environments:

#### 📸 4. Configured GitHub Repository Secrets
*Shows the encrypted repository secrets (`DEPLOY_KEY` and `API_TOKEN`) successfully configured in GitHub Settings.*
![GitHub Secrets](screenshots/04_github_secret.png)

#### 📸 5. Successful Staging Pipeline Execution (`staging` branch)
*Shows the automated graph execution for the `staging` branch: Install Dependencies -> Build Package -> Deploy to Staging.*
![GitHub Actions Staging](screenshots/05_github_actions_staging.png)

#### 📸 6. Successful Production Deployment (`v1.0.0` Release Tag)
*Shows the automated production pipeline triggered by publishing release tag `v1.0.0`: executing rigorous tests before deploying to the live Production server.*
![GitHub Actions Production](screenshots/06_github_actions_production.png)

---

## 🚀 Local Verification & Testing

To test and verify this repository locally on your macOS, Linux, or Windows workstation, execute the following commands:

### Step 1: Clone Repository
```bash
git clone https://github.com/kaushalpatil205/Flask-CI-CD-Pipeline.git
cd Flask-CI-CD-Pipeline
```

### Step 2: Initialize Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows PowerShell: .\venv\Scripts\Activate.ps1
```

### Step 3: Install Requirements & Run Test Suite
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov
pytest --maxfail=1 --disable-warnings -v
```

**Expected Test Output**:
```
============================= test session starts ==============================
collecting ... collected 3 items

test_app.py::test_basic_sanity PASSED                                    [ 33%]
test_app.py::test_flask_application_exists PASSED                        [ 66%]
test_app.py::test_environment PASSED                                     [100%]

============================== 3 passed in 0.02s ===============================
```

---

## 🏆 Conclusion & DevOps Best Practices

By completing this assignment, we have successfully implemented a dual CI/CD architecture that adheres to modern DevOps best practices:
1. **Automated Testing & Quality Gates**: No code can reach staging or production without passing automated unit tests (`pytest`).
2. **Environment Isolation**: Python virtual environments and Docker containerization guarantee reproducible builds across local machines, Jenkins servers, and GitHub cloud runners.
3. **Zero-Trust Secret Management**: Credential separation via GitHub Secrets ensures robust security during deployment automation.
4. **GitOps Workflow**: Clear branching strategies (`staging` vs. `main`) and release tagging (`v1.0.0`) govern the deployment lifecycle with complete traceability and audit logs.

---
*Submitted by **Kaushal Patil** (ID: `KaushalPatil_13408`, Email: `patilkaushal89@gmail.com`) for Hero Vired.*
