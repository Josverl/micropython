# Source: library\socket.rst:26
# Type: code_block
# Platform: unix
import socket

sockaddr = socket.getaddrinfo("www.micropython.org", 80)[0][-1]
# You must use getaddrinfo() even for numeric addresses
sockaddr = socket.getaddrinfo("127.0.0.1", 80)[0][-1]
# Now you can use that address
sock.connect(sockaddr)
