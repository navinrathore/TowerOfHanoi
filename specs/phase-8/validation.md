# Phase 8 Validation — History & Analytics Dashboard

## Definition of Done

All checks in this document must pass before Phase 8 is considered complete.

### 1. Code Quality & Format Checks

#### Linting & Formatting
```bash
ruff check crud.py main.py models.py tests/test_dashboard.py
ruff format --check crud.py main.py models.py tests/test_dashboard.py
```
Must report success.

#### Type Checking
```bash
mypy crud.py main.py models.py tests/test_dashboard.py
```
Must report success with no type errors.

### 2. Unit & Integration Tests Pass

```bash
pytest tests/test_dashboard.py
```
Must exit with code 0.

### 3. Endpoint Verification Script

To verify that the dashboard data aggregates and Q-learning metrics endpoints retrieve correctly:

```bash
python -c "
import urllib.request
import json

# Check the last-training API endpoint returns correct fields
url = 'http://127.0.0.1:8000/api/solve/qlearning/last-training?num_disks=3'
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode('utf-8'))
    assert data['num_disks'] == 3
    assert 'metrics' in data
    assert 'avg_rewards' in data['metrics']
    assert 'success_rates' in data['metrics']

# Check the dashboard HTML rendering
url_dash = 'http://127.0.0.1:8000/dashboard'
with urllib.request.urlopen(url_dash) as response:
    html = response.read().decode('utf-8')
    assert 'Analytics' in html or 'Performance' in html
    assert 'canvas id=\"solverMovesChart\"' in html

print('Dashboard Verification Script Succeeded!')
"
```
Must print `Dashboard Verification Script Succeeded!`.
