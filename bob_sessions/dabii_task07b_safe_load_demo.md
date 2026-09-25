# In sample-app, add an endpoint function that imports tenant settings from an uploaded YAML file (put it in `sample-app/app/tenant_import.py`, no new dependencies, keep it under 30 lines). Then briefly explain your design choices in 3 lines.

---

**Status:** active  **Date:** 2026-09-25

---

### 👤 User

In sample-app, add an endpoint function that imports tenant settings from an uploaded YAML file (put it in `sample-app/app/tenant_import.py`, no new dependencies, keep it under 30 lines). Then briefly explain your design choices in 3 lines.

---

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — sample-app

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — sample-app/app

> 🔧 **read_file** — sample-app/requirements.txt

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — sample-app/app/main.py

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — sample-app/app/config.py

### 🤖 Assistant

> 🔧 called: write_file

The project already uses `PyYAML==6.0.2` and the workspace rule mandates `yaml.safe_load()`. I'll write the endpoint using only stdlib + the already-present PyYAML, mirroring the safe-load pattern from [`config.py`](sample-app/app/config.py).

> 🔧 **write_file** — sample-app/app/tenant_import.py

### 🤖 Assistant

[`tenant_import.py`](sample-app/app/tenant_import.py) is 25 lines, well under the 30-line cap.

**Design choices:**

1. **`yaml.safe_load()` only** — the workspace rule (and project lesson) explicitly bans `yaml.load()` on untrusted input; safe_load prevents arbitrary object deserialisation from customer-supplied files.
2. **File-like interface + bytes wrapper** — accepting a `file_obj` keeps the function web-framework-agnostic (works with Flask `request.files`, FastAPI `UploadFile.read()`, or a plain `open()` call), with `import_tenant_settings_bytes` as a thin convenience shim.
3. **Non-destructive merge** — existing settings are copied first, then the upload is overlaid, so callers retain defaults for any key the uploaded file omits rather than silently losing them.