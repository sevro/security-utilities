use std::io::{BufReader, BufRead};
use std::fs::File;
use std::str::FromStr;
use clap::ArgMatches;
use std::net::{SocketAddr, SocketAddrV4, SocketAddrV6};
use subnet::*;


// TODO:
//  * verbosity to Enum
//  * Add -q --quiet
//
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
            Some("cidr") => {
                if let Some(subnet_matches) = matches.subcommand_matches("cidr") {
                    for subnet_str in subnet_matches.values_of("subnet").unwrap() {
                        let subnet = match Subnet::from_str(subnet_str) {
                            Ok(snet) => snet,
                            Err(_) => return Err("Invalid subnet provided"),
                        };

                        let mut ports: Vec<u16> = vec![];
                        if let Some(port_strs) = subnet_matches.values_of("ports") {
                            for port in port_strs {
                                match port.parse() {
                                    Ok(port) => ports.push(port),
                                    Err(_) => return Err("Invalid port provided"),
                                }
                            }
                        }

                        match subnet {
                            Subnet::V4(subnet) => {
                                for (ip, port) in subnet.into_iter().zip(ports.into_iter().cycle()) {
                                    sockets.push(SocketAddr::V4(SocketAddrV4::new(ip, port)));
                                }
                            }
                            Subnet::V6(subnet) => {
                                for (ip, port) in subnet.into_iter().zip(ports.into_iter()) {
                                    sockets.push(SocketAddr::V6(SocketAddrV6::new(ip, port, 0, 0)));
                                }
                            }
                        }
                    }
                }
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
