import network
import socket
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize the keyboard
kbd = Keyboard(usb_hid.devices)


# Number emulation functions
def presser(key):
    if key == "0":
        kbd.send(Keycode.ZERO)
    elif key == "1":
        kbd.send(Keycode.ONE)
    elif key == "2":
        kbd.send(Keycode.TWO)
    elif key == "3":
        kbd.send(Keycode.THREE)
    elif key == "4":
        kbd.send(Keycode.FOUR)
    elif key == "5":
        kbd.send(Keycode.FIVE)
    elif key == "6":
        kbd.send(Keycode.SIX)
    elif key == "7":
        kbd.send(Keycode.SEVEN)
    elif key == "8":
        kbd.send(Keycode.EIGHT)
    elif key == "9":
        kbd.send(Keycode.NINE)


# Wi-Fi credentials
ssid = "!!!SSID!!!"
password = "!!!PASSWORD!!!"


# HTML template for the webpage
def webpage():
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            Remote keypad
            <br>
            <br>
            <br>
        </head>
        <body>
            <form action="./1" id="keypadtop">
                <input type="submit" value="1" />
            </form>
            <form action="./2" id="keypadtop">
                <input type="submit" value="2" />
            </form>
            <form action="./3" id="keypadtop">
                <input type="submit" value="3" />
            </form>
            <br>
            <form action="./4" id="keypadtop">
                <input type="submit" value="4" />
            </form>
            <form action="./5" id="keypadtop">
                <input type="submit" value="5" />
            </form>
            <form action="./6" id="keypadtop">
                <input type="submit" value="6" />
            </form>
            <br>
            <form action="./7" id="keypadtop">
                <input type="submit" value="7" />
            </form>
            <form action="./8" id="keypadtop">
                <input type="submit" value="8" />
            </form>
            <form action="./9" id="keypadtop">
                <input type="submit" value="9" />
            </form>
            <br>
            <form action="./0" id="keypadtop">
                <input type="submit" value="0" />
            </form>
        </body>
        </html>
        <style>
            #keypadtop {
                display: inline-block;
            }
        </style>
    """
    return html


# Wi-Fi connecting snippet
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() >= 3:
        break
    connection_timeout -= 1
    print("Waiting for Wi-Fi connection...")
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError("Failed to establish a network connection")
else:
    print("Connection successful!")
    network_info = wlan.ifconfig()
    print("IP address:", network_info[0])

# Set up socket and start listening
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()

print("Listening", addr)

# Main loop to listen for connections
while True:
    try:
        conn, addr = s.accept()
        print("Got a connection from", addr)

        # Receive and parse the request
        request = conn.recv(1024)
        request = str(request)
        print("Request content = %s" % request)

        try:
            request = request.split()[1]
            print("Request:", request)
        except IndexError:
            pass

        # Process requests for specific numbers
        if request == "/1":
            print("Typing 1")
            presser("1")
        elif request == "/2":
            print("Typing 2")
            presser("2")
        elif request == "/3":
            print("Typing 3")
            presser("3")
        elif request == "/4":
            print("Typing 4")
            presser("4")
        elif request == "/5":
            print("Typing 5")
            presser("5")
        elif request == "/6":
            print("Typing 6")
            presser("6")
        elif request == "/7":
            print("Typing 7")
            presser("7")
        elif request == "/8":
            print("Typing 8")
            presser("8")
        elif request == "/9":
            print("Typing 9")
            presser("9")
        elif request == "/0":
            print("Typing 0")
            presser("0")

        # Generate HTML response
        response = webpage()

        # Send the HTTP response and close the connection
        conn.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print("Connection closed")
