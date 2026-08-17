# tar-zst-utils

CLI tool to compress, decompress, archive, and combine `.tar` and `.zst` (Zstandard) operations.

## Installation

```bash
pip install .
```

For development (editable mode):
```bash
pip install -e .
```

## Commands

| Command            | Aliases | Description |
|--------------------|---------|-------------|
| `decompress`       | `d`     | Decompress `.zst` → `.tar` |
| `extract`          | `e`     | Extract `.tar` archive to a directory |
| `decompress-extract`| `de`   | Decompress `.zst` and extract in one step |
| `compress`         | `c`     | Compress file to `.zst` |
| `archive`          | `a`     | Create `.tar` archive from a file |
| `archive-compress` | `ac`    | Archive and compress to `.tar.zst` in one step |

**Common options:**  
- `-o, --output <path>` – output file or directory (depends on command).  
- `-l, --level <1-22>` – compression level (default: 22, for `compress`/`archive-compress`).  
- `-t, --threads <N>` – threads (0 = all CPU, for `compress`/`archive-compress`).

## Examples

```bash
# Decompress .zst to .tar
tzu decompress archive.tar.zst

# Extract .tar to a custom folder
tzu extract archive.tar -o extracted/

# Decompress and extract at once
tzu decompress-extract archive.tar.zst -o out/

# Compress with level 10, 4 threads
tzu compress data.bin -l 10 -t 4 -o compressed.zst

# Create a .tar archive
tzu archive doc.pdf -o docs.tar

# Archive and compress in one step
tzu archive-compress photo.jpg -l 15 -t 2 -o photo.tar.zst
```

## Testing

```bash
pip install -e .[dev]
pytest tests/
```

## Dependencies

- Python ≥ 3.12
- [zstandard](https://github.com/facebook/zstd)
