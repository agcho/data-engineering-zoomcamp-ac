### Spark on GCP VM

## 1. Install Google Cloud CLI

> Download and install:
> https://cloud.google.com/sdk/docs/install

> gcloud --version

## 2. SSH to GCP VM
> gcloud auth login
> gcloud config set project YOUR_PROJECT_ID
> gcloud compute ssh VM_NAME --zone ZONE

## 3. Connect VS Code to GCP VM
> gcloud compute config-ssh
> VS Code → Remote-SSH: Connect to Host → select VM → choose Linux

## 4. Install PySpark
> sudo apt update
> sudo apt install -y openjdk-11-jdk-headless python3-venv python3-pip wget

> python3 -m venv pyspark-venv
> source pyspark-venv/bin/activate
> pip install pyspark jupyterlab ipykernel

## 5. Start Jupyter
> jupyter lab --no-browser --ip=127.0.0.1 --port=8888
> VS Code → PORTS → forward 8888