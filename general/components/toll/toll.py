import signal
import time
from components.toll.MFRC522 import MFRC522

class Toll:
    def __init__(self, toll_pin):
        self.MIFAREReader = MFRC522(toll_pin)
        self.previous_uid = None
        self.last_print = time.time()
        self.debounce_time = 5
        signal.signal(signal.SIGINT, self.end_read)

    def end_read(self, signal, frame):
        print("Ctrl+C captured, ending read.")
        self.destroy()
        
    def read_card(self):
        # Scan for cards    
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == self.MIFAREReader.MI_OK:
            print("Card detected")
            
            # Get the UID of the card
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == self.MIFAREReader.MI_OK:
                current_time = time.time()
                if uid != self.previous_uid or (current_time - self.last_print) > self.debounce_time:
                    # Print UID
                    print("Card read UID: " + ",".join(map(str, uid)))
                    self.previous_uid = uid
                    self.last_print = current_time
                    
                    # This is the default key for authentication
                    # key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    
                    # Select the scanned tag
                    # self.MIFAREReader.MFRC522_SelectTag(uid)

                    # Authenticate
                    # status = self.MIFAREReader.MFRC522_Auth(self.MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                    # Check if authenticated
                    # if status == self.MIFAREReader.MI_OK:
                    #     self.MIFAREReader.MFRC522_Read(8)
                    #     self.MIFAREReader.MFRC522_StopCrypto1()
                    # else:
                    #     print("Authentication error")

    def destroy(self):
        # destroy
        self.MIFAREReader.destroy()
        print("Toll system stopped.")


# Example usage
# if __name__ == "__main__":
#     toll = Toll()
#     try:
#         toll.read_card()
#     except KeyboardInterrupt:
#         toll.destroy()
