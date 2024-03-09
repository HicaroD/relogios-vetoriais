from typing import List
from threading import Thread
import time
import random
import socket
import ast

BUFFER_SIZE = 1024


class Process:
    def __init__(self, port: int, ports: List[int], number_of_ports: int) -> None:
        self.port = port
        self.vector = [0 for _ in range(number_of_ports)]
        # As portas de todos os processos estão armazenadas aqui
        # para que as mensagens possam ser enviadas aleatoriamente
        self.ports = ports

    def send(self):
        while 1:
            selected_port = random.choice(self.ports)
            if selected_port != self.port:
                self._set_random_delay()
                message = f"{self.port}:{self.vector}"
                print(
                    f"Enviando mensagem de {self.port} para {selected_port}: '{message}'"
                )
                send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                send_socket.sendto(
                    message.encode(),
                    ("localhost", selected_port),
                )

    def receive(self):
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive_socket.bind(("localhost", self.port))

        while 1:
            message, _ = receive_socket.recvfrom(BUFFER_SIZE)
            message = message.decode().split(":")
            sender_vector = ast.literal_eval(message[1])

            new_receiver_vector = [
                max(a, b)
                for a, b in zip(
                    self.vector,
                    sender_vector,
                )
            ]
            receiver_index = self.ports.index(self.port)
            new_receiver_vector[receiver_index] += 1

            print(
                f"Vetor recebido: {sender_vector}\n"
                f"Vetor antes da mensagem: {self.vector}\n"
                f"Vetor resultante: {new_receiver_vector}\n"
            )
            self.vector = new_receiver_vector

    def _set_random_delay(self):
        interval = random.uniform(1, 4)
        time.sleep(interval)


def main():
    ports = [5000, 5001, 5002, 5003]

    processes = []
    for port in ports:
        process = Process(port, ports, len(ports))
        processes.append(process)

    for process in processes:
        send_thread = Thread(target=process.send)
        receive_thread = Thread(target=process.receive)
        send_thread.start()
        receive_thread.start()


if __name__ == "__main__":
    main()
