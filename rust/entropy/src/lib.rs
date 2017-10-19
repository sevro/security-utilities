use std::error::Error;
use std::fs::File;
use std::io::{BufReader, Read};

pub struct Config {
    pub filename: String,
}

impl Config {
    pub fn new(mut args: std::env::Args) -> Result<Config, &'static str> {
        args.next();

        let filename = match args.next() {
            Some(filename) => filename,
            None => return Err("Didn't recieve an address:port"),
        };

        Ok(Config { filename })
    }
}

pub fn run(config: Config) -> Result<(), Box<Error>> {
    let file = match File::open(config.filename) {
        Ok(file) => file,
        Err(err) => return Err(Box::new(err)),
    };
    let mut reader = BufReader::new(file);

    let mut total_bytes = 0;
    let mut byte_counts = [0 as u64; 256];
    for byte in reader.bytes() {
        total_bytes += 1;
        match byte {
            Ok(b) => byte_counts[byte.unwrap() as usize] += 1,
            Err(err) => return Err(Box::new(err)),
        }
    }

    let mut entropy: f64 = 0.0;
    let mut probability: f64 = 0.0;
    for (idx, count) in byte_counts.iter().enumerate() {
        if *count == 0 { continue };
        probability = 1.0 * *count as f64 / total_bytes as f64;
        entropy -= probability * probability.log(256.0);
    }

    println!("Entropy: {}", entropy);

    Ok(())
}
