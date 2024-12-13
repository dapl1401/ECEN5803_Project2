import RPi.GPIO as GPIO
import time

# Define GPIO pin for the switch
SWITCH_PIN = 17  # GPIO pin 17

# Duration thresholds (in seconds): 
TIME_UNIT = 1  # 1 time unit = 0.2s
DOT_DURATION = TIME_UNIT  # Duration of a dot
DASH_DURATION = TIME_UNIT * 3  # Duration of a dash
INTRA_CHAR_DURATION = TIME_UNIT  # Gap between symbols (within the same letter)
INTER_CHAR_DURATION = TIME_UNIT * 3  # Gap between letters (within the same word)
WORD_DURATION = TIME_UNIT * 7  # Gap between words

# Morse code dict for A-Z and 0-9
MORSE_CODE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y", "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9"
}

morse_sequence = ""  # Buffer to store the current Morse code symbol sequence
decoded_message = ""  # Buffer to store the decoded text message

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering scheme
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin as input with pull-down resistor	

press_start_time = 0
press_release_time = 0
char_complete = False
word_complete = False

# Look up morse sequence from dict to get letter
def decode_morse_letter(morse_sequence):
    return MORSE_CODE.get(morse_sequence, '?')  # Return '?' if Morse sequence is invalid

# Check press duration to get symbol
def decode_press_morse_symbol(press_duration):
    if press_duration <= 3*DOT_DURATION/2:
        symbol = "."
    elif press_duration >= DASH_DURATION/2 and press_duration <= 3*DASH_DURATION/2 and press_duration < WORD_DURATION:
        symbol = "-"
    else:
        symbol = ""
    return symbol

# Check release duration to get symbol
def decode_release_morse_symbol(release_duration):
    global char_complete
    global word_complete
    if release_duration >= INTER_CHAR_DURATION and release_duration < WORD_DURATION:
        char_complete =  True
    elif release_duration >= WORD_DURATION:
        word_complete =  True
    else:
        char_complete = False
        word_complete = False
        
def morse_callback(channel):
    global decoded_message
    global morse_sequence
    global press_start_time
    global press_release_time
    
    if GPIO.input(SWITCH_PIN):
        press_start_time = time.time()  # Time when switch is pressed
        release_duration = time.time() - press_release_time # Time passed since switch was released
        print("Release duration:", str(release_duration))
        decode_release_morse_symbol(release_duration) # Release means intra-, inter-char or word gap
        if(char_complete): # Finished a morse sequence for a character
            char = decode_morse_letter(morse_sequence)
            decoded_message += char
            morse_sequence = "" # Reset morse sequence buffer
            print(f"Decoded Message: {decoded_message}")
        if(word_complete): # Finished characters for a word
            decoded_message += " "
            print(f"Decoded Message: {decoded_message}")

    else:
        press_release_time = time.time()  # Time when switch is released
        press_duration = time.time() - press_start_time # Time passed since switch was pressed
        print("Press duration:", str(press_duration))
        symbol = decode_press_morse_symbol(press_duration) # Press means symbol either dot or dash
        morse_sequence += symbol
        print(f"Morse sequence: {morse_sequence}")

# Run the Morse Code receiver

try:
    print("Morse Code Receiver Started")
    print("Press the switch to start generating Morse Code")
    GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=morse_callback, bouncetime=200)
    while True:
        x=0

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
finally:
    GPIO.cleanup()  # Clean up GPIO settings
