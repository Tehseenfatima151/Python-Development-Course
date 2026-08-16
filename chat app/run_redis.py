"""
Lightweight Redis Service for Windows & Development Environments
Runs a full Redis wire-compatible TCP server on 127.0.0.1:6379
"""
import sys
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("redis-server")

try:
    import fakeredis
except ImportError:
    print("fakeredis is required. Install via: pip install fakeredis")
    sys.exit(1)

def main():
    host = "127.0.0.1"
    port = 6379
    server = fakeredis.TcpFakeServer((host, port))
    server.daemon_threads = True
    print("=" * 55)
    print(f" [*] Redis TCP Server Running on {host}:{port}")
    print(" [*] Protocol: Redis Wire Protocol (RESP)")
    print(" [*] Status: READY FOR CONNECTIONS")
    print("=" * 55)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Redis server...")
        server.server_close()

if __name__ == "__main__":
    main()
