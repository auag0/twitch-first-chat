import requests
import time
import socket
import time

# twitch
streamer = "suteio"
message = "こんにちは!!"
authToken = "" # your token
name = "" # your display name

def sendChat():
    try:
        _socket = socket.socket()
        _socket.connect(("irc.chat.twitch.tv", 6667))
        _socket.send("CAP REQ :twitch.tv/tags twitch.tv/commands\n".encode("utf-8"))
        _socket.send(f"PASS oauth:{authToken}\n".encode("utf-8"))
        _socket.send(f"NICK {name}\n".encode("utf-8"))
        _socket.send(f"USER {name} 8 * :{name}\n".encode("utf-8"))
        _socket.send(f"JOIN #{streamer}\n".encode("utf-8"))
                    
        while True:
            resp = _socket.recv(2048).decode("utf-8")
            if "Welcome" in resp:
                _socket.send(f"PRIVMSG #{streamer} :{message}\n".encode("utf-8"))
            if f"display-name={name}" in resp and streamer in resp:
                print("成功")
                return

    except:
        print(f"再接続中")
        sendChat()
        time.sleep(1)
    finally:
        _socket.close()

def isLive(displayName):
    headers = {
        "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"
    }
    query = """
    query { 
        user(login: "__displayName__") { 
            stream { 
                id 
            } 
        } 
    }
    """.replace("__displayName__", displayName)
    response = requests.post("https://gql.twitch.tv/gql", headers=headers, json={"query": query}, timeout=10)
    try:
        response.json()["data"]["user"]["stream"]["id"]
    except:
        return False
    return True

already = False
if __name__ == "__main__":
    while True:
        if not already:
            time.sleep(4)
            if isLive(streamer):
                print("live")
                sendChat()
                already = True
