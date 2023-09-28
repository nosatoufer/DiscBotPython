import bot
import multiprocessing
import http.server
import os 

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

# This is for health check
def run():
    port = int(os.environ.get('PORT') or 10000) 
    server_address = ('0.0.0.0', port)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    httpd.serve_forever()


def run_discord_bot():
    bot.run_discord_bot()


if __name__ == '__main__':
    
    socket_server_process = multiprocessing.Process(target=run)
    discord_bot = multiprocessing.Process(target=run_discord_bot)

    socket_server_process.start()
    discord_bot.start()

    socket_server_process.join()
    discord_bot.join()