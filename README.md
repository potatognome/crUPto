
# crUPto (v0.7.0)

Cryptocurrency portfolio tracking and tax reporting utility with multi-wallet support and automated PDF extraction


## Configuration (v0.7.0 and later)

## New in v0.7.0

- **Live Terminal Status Table**: Real-time, in-place status/progress table for staking and multi-asset operations, powered by tUilKit's new terminal modules (Canvas, Cursor, Chroma).

---

## Installation

### Development Installation

For development, install in editable mode:

```bash
cd crUPto
pip install -e .
```

This allows you to:
- Run the project as a module: `python -m crUPto`
- Use the console script: `crUPto`
- Make changes to the code without reinstalling

### Standard Installation

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Using the root-level runner (no installation needed)

```bash
python crUPto.py
```

### Option 2: As a module (after pip install -e .)

```bash
python -m crUPto
```

### Option 3: Using console script (after pip install -e .)

```bash
crUPto
```
