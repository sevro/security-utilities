use std::error::Error;
use std::str::FromStr;

use std::time::Duration;
use std::net::{SocketAddr, TcpStream};

pub struct Config {
    pub socket_addr: SocketAddr,
}

impl Config {
    pub fn new(mut args: std::env::Args) -> Result<Config, &'static str> {
        args.next();

        let socket_addr = match args.next() {
            Some(arg) => 
                match SocketAddr::from_str(&arg) {
                    Ok(socket_addr) => socket_addr,
                    Err(_) => return Err("Invalid address:port"),
                },
            None => return Err("Didn't recieve an address:port"),
        };

        Ok(Config { socket_addr })
    }
}

pub fn run(config: Config) -> Result<(), Box<Error>> {

    let result;
    if let Ok(stream) = TcpStream::connect_timeout(&config.socket_addr, Duration::new(2, 0)) {
        result = "open";
    } else {
        result = "closed";
    }
    
    println!("Port {} is {}", config.socket_addr, result);

    Ok(())
}
