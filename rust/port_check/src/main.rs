//! port_check
//!
//! Checks if a single port is open and prints the result.

extern crate port_check;

use std::env;
use std::process;

use port_check::Config;

fn main() {
    let config = Config::new(env::args()).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {}", err);
        process::exit(1);
    });

    if let Err(err) = port_check::run(config) {
        eprintln!("Application error: {}", err);
        process::exit(1);
    }
}
