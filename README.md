
```markdown
# MLflow Experiment Tracking Practice

A hands-on implementation of MLflow for machine learning experiment tracking, covering both local tracking workflows and remote artifact and metric logging with DagsHub.

---

## Overview

This repository demonstrates how to track parameters, metrics, and models using MLflow. It covers two execution workflows:
1. **Local Tracking**: Logging runs to a local directory or SQLite backend and viewing runs via the local MLflow UI.
2. **Remote Tracking**: Directing logs and model artifacts to a hosted DagsHub remote MLflow server.

---

## Project Structure

```text
├── .env                 # Environment variables for DagsHub credentials
├── .gitignore           # Git ignore file for virtualenv, logs, and sensitive files
├── requirements.txt     # Python dependencies
├── app.py               # Main training and tracking script
└── README.md            # Project documentation

```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone [https://github.com/Rajkumar-Ai-Engineer/MLFLOW.git](https://github.com/Rajkumar-Ai-Engineer/MLFLOW.git)
cd MLFLOW

```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

---

## Environment Configuration

Create a `.env` file in the root directory if you are connecting to DagsHub:

```env
MLFLOW_TRACKING_URI=[https://dagshub.com/](https://dagshub.com/)<username>/<repo_name>.mlflow
MLFLOW_TRACKING_USERNAME=<your_dagshub_username>
MLFLOW_TRACKING_PASSWORD=<your_dagshub_token>

```

> **Security Note:** Never commit your `.env` file to remote version control. Ensure `.env` is included inside `.gitignore`.

---

## Usage

### Workflow 1: Local MLflow Tracking

Run the training pipeline locally:

```bash
python app.py

```

Launch the MLflow user interface in your terminal:

```bash
mlflow ui

```

Access the dashboard in your browser at `http://127.0.0.1:5000`.

---

### Workflow 2: Remote Tracking via DagsHub

Initialize DagsHub tracking directly inside `app.py` or export your credentials into the shell session:

```python
import os
import dagshub
import mlflow

dagshub.init(repo_owner='<username>', repo_name='<repo_name>', mlflow=True)

with mlflow.start_run():
    mlflow.log_param("alpha", 0.5)
    mlflow.log_metric("rmse", 0.78)

```

Run your script:

```bash
python app.py

```

All parameters, metrics, and artifacts will synchronize directly to your DagsHub repository's MLflow tab.

---

## What Gets Tracked

* **Hyperparameters:** Model-specific configurations like learning rate, estimators, and regularization strength.
* **Metrics:** Evaluation scores such as RMSE, MAE, R², or accuracy.
* **Artifacts:** Serialized model binaries, plots, confusion matrices, and feature importance charts.

```

```
