# Running the Backend

## Windows (Recommended)

**Do NOT use `--reload` flag on Windows** - it causes socket permission errors (WinError 10013).

### Option 1: Using the batch script
```cmd
cd backend
run.bat
```

### Option 2: Direct command (without --reload)
```cmd
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Option 3: Using PowerShell
```powershell
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Linux/Mac

You can use `--reload` for auto-reload during development:

```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Or use the provided script:
```bash
bash run_dev.sh
```

## Accessing the API

Once running, the API will be available at:

- **API Base**: http://127.0.0.1:8000
- **Swagger Docs**: http://127.0.0.1:8000/docs
- **ReDoc Docs**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## Default Credentials

```
Email: admin@ahadubank.com
Password: password123
Role: super_admin
```

## Troubleshooting

If you see: `WinError 10013 - An attempt was made to access a socket in a way forbidden by its access permissions`

1. Remove `--reload` flag from the command
2. Kill any existing Python processes: `Get-Process python | Stop-Process -Force`
3. Wait a few seconds
4. Start again without `--reload`
