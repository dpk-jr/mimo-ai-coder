# MiMo AI Coder

Multi-file AI pair programmer — analyze, refactor, test, and migrate codebases.

> MiMo 100T Program — showcasing MiMo-V2.5-Pro's code intelligence

---

## What Makes This Different

Other AI coders work file-by-file. MiMo AI Coder understands **entire projects**:
- Reads dependency graphs across files
- Maintains context during multi-file refactoring
- Generates tests that cover edge cases
- Migrates code between languages preserving semantics

## Features

| Command | Description |
|---------|-------------|
| `analyze <dir>` | Project-wide analysis: complexity, dependencies, dead code |
| `refactor <file>` | AST-aware refactoring: extract method, rename, inline |
| `tests <file>` | Generate comprehensive test suites with edge cases |
| `migrate <file>` | Cross-language migration (Python to TypeScript, REST to GraphQL) |

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env

python main.py analyze ./my-project
python main.py refactor src/utils.py --action extract-method --lines 15-30 --name "parse_config"
python main.py tests src/api.py --framework pytest
python main.py migrate src/models.py --from python --to typescript
```

## Why MiMo-V2.5-Pro?

1. **Project Context**: Reads 10+ files simultaneously (128K context)
2. **Code Understanding**: Native AST comprehension across languages
3. **Refactoring Intelligence**: Suggests changes that maintain behavior
4. **Test Quality**: Generates tests humans would actually write

---

*Powered by Xiaomi MiMo-V2.5-Pro*
