#!/bin/bash
source ~/rust_python_test/.venv/bin/activate
cargo install --locked --root ~/.cargo maturin || echo "maturin already cached"
maturin develop
python -c "import rust_python_test; print(rust_python_test.hello())"
