//! pingsweep 
//!
//! Checks if a single port is open and prints the result.

#[macro_use]
extern crate clap;
extern crate pingsweep;

use std::process;
use clap::App;
use pingsweep::Config;

fn main() {

    let yaml = load_yaml!("../resources/cli.yml");
    let app = App::from_yaml(yaml)
        .name(crate_name!())
        .author(crate_authors!())
        .about(crate_description!())
        .version(crate_version!());

    let config = Config::new(app.get_matches()).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {}", err);
        process::exit(1);
    });

    if let Err(err) = pingsweep::run(config) {
        eprintln!("Application error: {}", err);
        process::exit(1);
    }
}
