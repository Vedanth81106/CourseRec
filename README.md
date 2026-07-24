# CourseRec Setup

## 1. Create a Virtual Environment

Run the appropriate command for your operating system:

**Windows**

```bash
python -m venv venv
```

**Linux / macOS**

```bash
python3 -m venv venv
```

## 2. Activate the Virtual Environment

**Windows (Command Prompt)**

```bash
venv\Scripts\activate
```

**Windows (PowerShell)**

```powershell
venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source venv/bin/activate
```

> **Note:** Once the virtual environment is activated, your terminal prompt will display something similar to `(venv)`.

## 3. Install Project Dependencies

From the project's root directory, run:

```bash
pip install -r requirements.txt
```
