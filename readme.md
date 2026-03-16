Distributed Clock Synchronization System using UDP

Description
This project implements a distributed clock synchronization system using UDP socket programming.
A central server provides timestamps, and multiple clients synchronize their clocks based on the
calculated network delay and clock offset.

Components

1. server.py – Time server that responds to client requests.
2. client.py – Client that requests timestamps and synchronizes its clock.
3. results.txt – Performance evaluation and observations.

How to Run

1. Run the server:
   python server.py

2. Run the clients:
   python client.py

3. Enter unique Client IDs for each client.

Features

- UDP socket communication
- Clock synchronization using timestamp exchange
- Network delay and clock offset calculation
- Multi-client testing

Performance Results
Multiple clients were tested simultaneously.
Average network delay remained around 0.001–0.002 seconds and synchronization was successful.
