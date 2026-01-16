import socket
import threading
import random

from server import Server

#AI generated
HOST = "0.0.0.0"
PORT = 65530
TIMEOUT = 5

bank_ip = None
accounts = {}  # account_number -> balance
lock = threading.Lock()


def handle_client(conn, addr):
    conn.settimeout(TIMEOUT)
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                command = data.decode("utf-8").strip()
                response = process_command(command)
                conn.sendall((response + "\n").encode("utf-8"))

            except socket.timeout:
                conn.sendall(b"ER Timeout\n")
                break
            except Exception:
                conn.sendall(b"ER Internal error\n")
                break


def process_command(cmd: str) -> str:
    parts = cmd.split()

    if not parts:
        return "ER Empty command"

    code = parts[0].upper()

    if code == "BC":
        return f"BC {bank_ip}"

    if code == "AC":
        with lock:
            while True:
                acc = random.randint(10000, 99999)
                if acc not in accounts:
                    accounts[acc] = 0
                    return f"AC {acc}/{bank_ip}"

    if code == "AD":
        try:
            acc_part, amount = parts[1], int(parts[2])
            acc, ip = acc_part.split("/")
            acc = int(acc)
        except Exception:
            return "ER Invalid format"

        if ip != bank_ip:
            return "ER Foreign bank not supported"

        with lock:
            if acc not in accounts:
                return "ER Account not found"
            accounts[acc] += amount
        return "AD"

    if code == "AW":
        try:
            acc_part, amount = parts[1], int(parts[2])
            acc, ip = acc_part.split("/")
            acc = int(acc)
        except Exception:
            return "ER Invalid format"

        if ip != bank_ip:
            return "ER Foreign bank not supported"

        with lock:
            if acc not in accounts:
                return "ER Account not found"
            if accounts[acc] < amount:
                return "ER Not enough funds"
            accounts[acc] -= amount
        return "AW"

    if code == "AB":
        try:
            acc, ip = parts[1].split("/")
            acc = int(acc)
        except Exception:
            return "ER Invalid format"

        if ip != bank_ip:
            return "ER Foreign bank not supported"

        with lock:
            if acc not in accounts:
                return "ER Account not found"
            return f"AB {accounts[acc]}"

    return "ER Unknown command"


def main():
    global bank_ip

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        bank_ip = socket.gethostbyname(socket.gethostname())

        print(f"Bank node running on {bank_ip}:{PORT}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    server = Server("0.0.0.0", 65530, 5)