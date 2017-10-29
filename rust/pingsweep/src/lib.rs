extern crate clap;
extern crate subnet;
pub mod config;

use std::time::Duration;
use std::sync::{Mutex, Arc};
use std::thread;
use std::error::Error;
use std::net::TcpStream;
use self::config::Config;

pub fn run(config: Config) -> Result<(), Box<Error>> {
    
    let mut handles = vec![];
    let sockets = Arc::new(Mutex::new(config.sockets));
    for i in 0..config.threads {
        let sockets = sockets.clone();
        let handle = thread::spawn(move || {
            loop {
                let address = match sockets.lock().unwrap().pop() {
                    Some(address) => address,
                    None => break,
                };

                // FIXME: 
                // Considers _any_ response to be up
                // Even ICMP: Destination Host Unreachable
                if let Ok(_stream) = TcpStream::connect_timeout(&address, Duration::new(2, 0)) {
                    println!("[{}] Address {} is up", i, address.ip());
                } else {
                    println!("[{}] Address {} is down", i, address.ip());
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
