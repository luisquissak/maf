# Create venv
```bash
py -m venv .venv
.venv\scripts\activate
```


# Install
```bash
pip install -U agent-framework --pre
```

# Login
```bash
az login
```

# Load var
```bash
get-content .env | foreach {
    $name, $value = $_.split('=')
    set-content env:\$name $value
    echo $name $value
}
```

# run

```bash
.venv\scripts\activate
python .\src\ag1.py
```

# Refs

- [Microsoft Agent Framework Quick-Start Guide](https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start?pivots=programming-language-python)
