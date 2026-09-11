# CRC Error Detection System

A simple B.Tech lab project that demonstrates Cyclic Redundancy Check using Python and Streamlit.

## Features

- Binary, text, and file input
- CRC calculation and codeword generation
- CRC verification for received data
- One-bit error simulation
- CRC-3, CRC-4, CRC-8, and CRC-32 choices
- Testing page and session history

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How it works

The program appends zeros to the input. It divides that value by the generator polynomial using XOR instead of normal subtraction. The final remainder is the CRC. The sender transmits the original data plus this remainder. The receiver repeats the division: a zero remainder means no error was detected.

The workspace was empty before this project was created, so there was no previous CRC implementation to preserve.