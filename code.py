import socketpool
import wifi
import ipaddress
import mdns
from adafruit_httpserver import Server, Request, FileResponse, Response, POST
import json

# Defining colors for a pretty output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'  # Removed the trailing backslash

# Start the access point where users should connect to
AP_SSID = "PicoChat"
AP_PASSWORD = "password"

print("")
print("===================================")
print(f"{bcolors.BOLD}Starting PicoChat UwU{bcolors.ENDC}")
print("===================================")
print("")
print("Creating access point...")

wifi.radio.start_ap(ssid=AP_SSID)
print(f"{bcolors.OKGREEN}Acess Point created : {AP_SSID} {bcolors.ENDC}")

pool = socketpool.SocketPool(wifi.radio)

# Configure IP address
ipv4 =  ipaddress.IPv4Address("192.168.1.10")
netmask =  ipaddress.IPv4Address("255.255.255.0")
gateway =  ipaddress.IPv4Address("192.168.1.1")
wifi.radio.set_ipv4_address_ap(ipv4=ipv4, netmask=netmask, gateway=gateway)

print("IP address is : "+str(wifi.radio.ipv4_address_ap))

# Configure mDNS
# TODO : Fix it :)
try:
    mdns_server = mdns.Server(wifi.radio)
    mdns_server.hostname = "chat"
    mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=5000)
except RuntimeError as e:
    print("MDNS setting failed:", str(e))

# Configuring webpage
def webpage():
    messages_html = "".join([f"<p><strong>{msg['username']}:</strong> {msg['message']}</p>" for msg in messages])
    html = f"""
    <!doctype html>
    <html>
        <head>
            <title>PicoChat</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <style>
                h1 {{
                    text-align: center;
                }}
                html {{
                    height: 100%;
                }}
                body {{
                    background-color: #000000;
                    color: #ffffff;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                .text {{
                    color: #ffffff;
                    text-align: center;
                    font-size: 2em;
                    margin-top: 20%;
                }}
                #message {{
                    background-color: #ffffff;
                    border: none;
                    padding: 10px;
                    color: #000000;
                    width: 80%;
                }}
                #send {{
                    background-color: #AAAAAA;
                    border: none;
                    padding: 10px;
                    color: #000000;
                    width: 20%;
                }}
                #form {{
                    position: fixed;
                    bottom: 0;
                    display: flex;
                    flex-direction: row;
                    width: 100%;
                }}
            </style>
        </head>
        <body>
            <script>
            async function sendData() {{
                const message = document.querySelector("#message").value;
                const username = document.cookie.split("=")[1];
                const response = await fetch("/", {{
                    method: "POST",
                    body: JSON.stringify({{ username, message }})
                }});
                document.querySelector("#message").value = "";
                location.reload();
            }}

            window.addEventListener("DOMContentLoaded", (event) => {{
                const send = document.getElementById("send");
                send.addEventListener("click", sendData);

                if (!document.cookie) {{
                    const username = prompt("Please enter your username");
                    document.cookie = `username=${{username}}`;
                }} else {{
                    const username = document.cookie.split("=")[1];
                }}

            }});
            </script>
            <div id="messages">
            {
                messages_html
            }
            </div>
            <div id="form">
                <input
                    id="message"
                    placeholder="Type your message here"
                />
                <button id="send">Send</button>
            </div>
        </body>
    </html>
    """
    return html

# Start the server
server = Server(pool, "/static", debug=True)

# Define message dictionary
messages = [
    {"username": "system", "message": "Server started!"},
    {"username": "system", "message": "Welcome to PicoChat!"},
]

@server.route("/")
def base(request: Request):
    return Response(request, f"{webpage()}", content_type='text/html')

# Handle POST requests to add a message
@server.route("/", POST)
def buttonpress(request: Request):
    #  get the raw text
    print(request.json())
    result = request.json()
    messages.append(result)
    return Response(request, f"{webpage()}", content_type='text/html')

server.serve_forever(str(wifi.radio.ipv4_address_ap))
