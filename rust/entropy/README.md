# Entropy

Check the entropy of a file.

## Usage

- Input: A file path
- Output: entropy of the file.

To compile and run, the result may be in `debug` or `release` depending on how it was compiled:

```sh
cargo build
./target/debug/entropy README.md
Entropy: 0.6182212973203925
```

Optionally run directly:

```sh
cargo run some_file.zip
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/entropy some_file.zip`
Entropy: 0.9984496192704049
```

Compile with `--release` if any sort of performance on large files is needed.
