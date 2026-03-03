## Create and Use a Python Virtual Environment (Windows)

Using a virtual environment keeps project dependencies isolated and avoids conflicts with system Python.

### Prerequisites

* Python **3.11 or higher**
* Python added to **PATH**

Verify:

```powershell
python --version
```

---

### Step 1: Create a Virtual Environment

From the project root directory:

```powershell
python -m venv .venv
```

This creates a `.venv` folder containing an isolated Python environment.

---

### Step 2: Activate the Virtual Environment

```powershell
.venv\Scripts\activate
```

You should see `(.venv)` at the beginning of your terminal prompt.

---

### Step 3: Upgrade pip (Recommended)

```powershell
python -m pip install --upgrade pip
```

---

### Step 4: Install Project Dependencies

For this project (dlt + DuckDB):

```powershell
pip install "dlt[workspace]"
```

---

### Step 5: Run the Pipeline

```powershell
python dlt_taxi_pipeline.py
```

---

### Setp 6: Open dlt dashboard

```dlt
dlt pipeline taxi_pipeline show
```

### Step 6: Deactivate the Virtual Environment (Optional)

```powershell
deactivate
```

---
