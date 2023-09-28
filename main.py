import bot
import multiprocessing
import socket
import os 

# This is for render
def run_socket_server():
    port = os.environ.get('PORT') or "8080"
    mytcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mytcp.bind(('0.0.0.0', port))
    mytcp.listen(1)
    while(1):
        mytcp.listen(1)


def run_discord_bot():
    bot.run_discord_bot()


if __name__ == '__main__':

    socket_server_process = multiprocessing.Process(target=run_socket_server)
    discord_bot = multiprocessing.Process(target=run_discord_bot)

    socket_server_process.start()
    discord_bot.start()

    socket_server_process.join()
    discord_bot.join()