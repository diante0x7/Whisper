# Whisper
Whisper is a covert data transmission tool, intended for use in offensive security or intelligence operations to transmit sensitive information quickly and privately over short distances.

## Why Whisper?
Bluetooth Low Energy can be leveraged to transmit data over short distances without triggering common IDS/IPS systems or being noisy; our phones, watches, and pacemakers emit information over the protocol 24/7. By simulating a proprietary Bluetooth protocol, we are able to accomplish our goal of covert communication, whether we are sending messages to each other, performing data exfiltration during a pentest, or whatever your imagination desires!

## Setup && Usage
Whisper is very easy to deploy, although I recommend you use Living-Off-The-Land to run the transmitter in memory.

### Setup
```bash
git clone https://github.com/diante0x7/Whisper.git
cd Whisper
pip install -r requirements.txt
```
### Usage
Usage is very simple! For the current Proof-Of-Concept version we will only be transmitting files. To do so:
```bash
python whisper.py <filename>
```

## Features
- 2-way handshake to identify the corresponding receiver-transmitter pair before transmitting sensitive data
- UUID emulation and digital signature verification to make most scanners unaware of Whisper's activity
- Self destructs after use, cleaning up itself as well as any mentions of it within logfiles on **ANY** platform.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.