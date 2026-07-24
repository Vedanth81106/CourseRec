# CourseRec Setup

## 1. Create a Virtual Environment

Run the appropriate command for your operating system.

### Windows

```bash
python -m venv venv
```

### Linux / macOS

```bash
python3 -m venv venv
```

---

## 2. Activate the Virtual Environment

### Windows (Command Prompt)

```bash
venv\Scripts\activate
```

### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source venv/bin/activate
```

> **Note:** Once the virtual environment is activated, your terminal prompt should display something similar to `(venv)`.

---

## 3. Install Project Dependencies

From the project's root directory, install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 4. Create the PostgreSQL Database

### Open PostgreSQL

* **Windows:** Open the **psql** command-line tool.
* **Linux / macOS:** Run:

```bash
psql -U <postgres_username>
```

### Create the database

```sql
CREATE DATABASE courserec;
```

### Verify the database

Run the following command:

```sql
\l
```

You should see `courserec` listed among the available databases.

---

## 5. Configure Environment Variables

Create a `.env` file in the project's root directory and add the following:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/courserec
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

---

## 6. Update `.gitignore`

Before pushing the project to GitHub, ensure your `.gitignore` file contains the following entries:

```gitignore
venv/
.venv/
__pycache__/
.env
*.pyc
```

> **Note:** Include `venv/` if your virtual environment is named `venv`, and `.venv/` if it is named `.venv`.

---

## Setup Complete

Once all of the above steps are complete, you're ready to run the project. Make sure your virtual environment is activated before starting the application.
# CourseRec Setup

## 1. Create a Virtual Environment

Run the appropriate command for your operating system.

### Windows

```bash
python -m venv venv
```

### Linux / macOS

```bash
python3 -m venv venv
```

---

## 2. Activate the Virtual Environment

### Windows (Command Prompt)

```bash
venv\Scripts\activate
```

### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source venv/bin/activate
```

> **Note:** Once the virtual environment is activated, your terminal prompt should display something similar to `(venv)`.

---

## 3. Install Project Dependencies

From the project's root directory, install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 4. Create the PostgreSQL Database

### Open PostgreSQL

* **Windows:** Open the **psql** command-line tool.
* **Linux / macOS:** Run:

```bash
psql -U <postgres_username>
```

### Create the database

```sql
CREATE DATABASE courserec;
```

### Verify the database

Run the following command:

```sql
\l
```

You should see `courserec` listed among the available databases.

---

## 5. Configure Environment Variables

Create a `.env` file in the project's root directory and add the following:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/courserec
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

---

## 6. Update `.gitignore`

Before pushing the project to GitHub, ensure your `.gitignore` file contains the following entries:

```gitignore
venv/
.venv/
__pycache__/
.env
*.pyc
```

> **Note:** Include `venv/` if your virtual environment is named `venv`, and `.venv/` if it is named `.venv`.


