extern crate clap;

use std::time::Duration;
use std::sync::{Mutex, Arc, MutexGuard};
use std::thread;
use std::io::{BufReader, BufRead};
use std::fs::File;
use std::str::FromStr;
use std::error::Error;
use std::net::{SocketAddr, TcpStream};
use clap::ArgMatches;

// TODO: verbosity to Enum
pub struct Config {
    pub verbosity: u8,
    pub threads: u64,
    pub sockets: Vec<SocketAddr>,
}

impl Config {
    pub fn new(matches: ArgMatches) -> Result<Config, &'static str> {
        let verbosity = Config::parse_verbosity(&matches);

        let threads = match matches.value_of("threads").unwrap_or("1").parse() {
            Ok(num) => num,
            Err(_) => return Err("Threads must be an integer"),
        };

        let mut sockets = vec![];
        match matches.subcommand_name() {
            Some("list") => {
                if let Some(socket_addrs) = matches.subcommand_matches("list") {
                    for socket_str in socket_addrs.values_of("sockets").unwrap() {
                        let socket_addr = match SocketAddr::from_str(socket_str) {
                            Ok(socket_addr) => socket_addr,
                            Err(_) => return Err("Invalid address provided"),
                        };
                        sockets.push(socket_addr);
                    }
                };
            },
            Some("file") => {
                if let Some(input_file) = matches.subcommand_matches("file") {
                    let f = match File::open(input_file.value_of("FILE").unwrap()) {
                        Ok(f) => f,
                        Err(_) => return Err("Unable to open file"),
                    };

                    let file = BufReader::new(f);

                    for line in file.lines() {
                        let socket_addr = match SocketAddr::from_str(line.unwrap().trim()) {
                            Ok(socket_addr) => socket_addr,
                            Err(e) => {
                                println!("{}", e);
                                return Err("Invalid address provided")
                            },
                        };
                        sockets.push(socket_addr);
                    }
                };
            },
            Some(&_) | None => return Err("See usage"),
        }

        Ok(Config { verbosity, sockets, threads })
    }

    fn parse_verbosity(matches: &ArgMatches) -> u8 {
        if matches.is_present("verbosity") {
            matches.occurrences_of("verbosity") as u8
        } else {
            1
        }
    }
}

pub fn run(config: Config) -> Result<(), Box<Error>> {
    
    let mut handles = vec![];
    let sockets = Arc::new(Mutex::new(config.sockets));
    for _ in 0..config.threads {
        let sockets = sockets.clone();
        let handle = thread::spawn(move || {
            loop {
                let address = match sockets.lock().unwrap().pop() {
                    Some(address) => address,
                    None => break,
                };

                if let Ok(stream) = TcpStream::connect_timeout(&address, Duration::new(2, 0)) {
                    println!("[*] Port {} is open", address);
                } else {
                    println!("[*] Port {} is closed", address);
                };
            }
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    Ok(())
}
