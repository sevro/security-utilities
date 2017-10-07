# Port Check

Check if a single port is open.

## Build

Nightly toolchain required currently for `connect_timeout` on the stream.

## Usage

- Input: A IP address and port number formatted as `127.0.0.1:8000`.
- Output: Open or closed

To compile and run, the result may be in `debug` or `release` depending on how it was compiled:


```sh
./target/debug/port_check 104.20.208.3:80
Port 104.20.208.3:80 is open
./target/debug/port_check 8.8.8.8:80
Port 8.8.8.8:80 is closed
```

Optionally run directly:

```sh
cargo run --release 127.0.0.1:8000                                                           INSERT  13:45:41 
   Compiling port_check v0.1.0 ()
    Finished release [optimized] target(s) in 1.23 secs
     Running `target/release/port_check '127.0.0.1:8000'`
Port 127.0.0.1:8000 is open
```
