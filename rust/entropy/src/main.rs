//! Entropy
//!
//! Check the entropy of a file.

extern crate entropy;

use std::env;
use std::process;

use entropy::Config;

fn main() {
    let config = Config::new(env::args()).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {}", err);
        process::exit(1);
    });

    if let Err(err) = entropy::run(config) {
        eprintln!("Application error: {}", err);
        process::exit(1);
    }
}
