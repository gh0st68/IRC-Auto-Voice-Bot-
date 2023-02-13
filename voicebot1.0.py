import socket
import ssl
import time
import sys

##voice bot made by gh0st##
##irc.twistednet.org #twisted

#How to use
# The command "$von" turns on auto voice
# The command "$voff" turns off auto voice
# The command "$voice" will voice all exisitng users in a channel.
# One day I will make this more easy.
# But for now if you wish to change the bots name you must change it in the irc.sock section and here elif ircmsg.find("001 sp00kb0t") != -1:


# Set the standard output encoding to UTF-8
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)




ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




# Create an SSL context with default settings
context = ssl.create_default_context()




# Wrap the socket in the context, providing the server hostname as an argument
ircsock = context.wrap_socket(ircsock, server_hostname="irc.twistednet.org")




ircsock.connect(("irc.twistednet.org", 6697))
ircsock.send(bytes("NICK sp00kb0t\r\n", "UTF-8"))
ircsock.send(bytes("USER sp00kb0t 0 * :sp00kb0t\r\n", "UTF-8"))




auto_voice = False




def ping(ircmsg):
  # Extract the cookie value from the PING request
  cookie = ircmsg.split(":")[1]
  # Send the PONG response back to the server
  ircsock.send(bytes("PONG :" + cookie + "\n", "UTF-8"))




def voice_users(channel):
  print("Getting list of users in channel", channel)
  ircsock.send(bytes("NAMES " + channel + "\r\n", "UTF-8"))
  ircmsg = ircsock.recv(2048).decode("UTF-8")
  while ircmsg.find("End of /NAMES list.") == -1:
      ircmsg += ircsock.recv(2048).decode("UTF-8")
  print("Received list of users:", ircmsg)
  users = ircmsg.split(" ")
  users_to_voice = [user for user in users if not any(c in user[0] for c in ["~", "&", "@", "+", "%"])]
  print("Users to voice:", users_to_voice)
  for user in users_to_voice:
      ircsock.send(bytes("MODE " + channel + " +v " + user + "\r\n", "UTF-8"))
      print("Voiced user:", user)
      time.sleep(1)




def voice_new_user(channel, user):
  print("Voicing user:", user)
  ircsock.send(bytes("MODE " + channel + " +v " + user + "\r\n", "UTF-8"))




channel = "#Twisted"




while True:
  ircmsg = ircsock.recv(2048).decode("UTF-8")
  ircmsg = ircmsg.strip('\n\r')
  print("Received message:", ircmsg)


  if ircmsg.find("PING :") != -1:
      ping(ircmsg)
  elif ircmsg.find("001 sp00kb0t") != -1:
      # 001 is the code for welcome message
      # we join the channel after we receive the welcome message
      ircsock.send(bytes("JOIN " + channel + "\r\n", "UTF-8"))
  elif "$voice" in ircmsg and ircmsg.find("PRIVMSG " + channel) != -1:
      print("Received $voice command in channel:", channel)
      voice_users(channel)
  elif ircmsg.find("JOIN :" + channel) != -1 and auto_voice:
      # voice user when they join the channel
      user = ircmsg.split('!')[0][1:]
      voice_new_user(channel, user)
  elif "$voff" in ircmsg and ircmsg.find("PRIVMSG " + channel) != -1:
      print("Disabling auto voicing of users who join the channel")
      auto_voice = False
      ircsock.send(bytes("PRIVMSG " + channel + " :Auto-Voice Disabled\n", "UTF-8"))
  elif "$von" in ircmsg and ircmsg.find("PRIVMSG " + channel) != -1:
      print("Enabling auto voicing of users who join the channel")
      auto_voice = True
      ircsock.send(bytes("PRIVMSG " + channel + " :Auto-Voice Enabled\n", "UTF-8"))
  else:
      print("Ignoring message")