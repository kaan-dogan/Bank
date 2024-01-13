# Kaya Bank System

This is a simple banking system implemented in Python using the Tkinter library for the graphical user interface and MySQL as the database for storing user information and transactions.

[![Project Status](https://img.shields.io/badge/status-unfinished-yellow)](https://github.com/yourusername/yourproject)

## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Setup

1. **Database Configuration:**
   - Ensure that you have MySQL installed and running.
   - Open `bank_system.py` and update the database connection details in the `mysql.connector.connect` section with your MySQL credentials.

2. **Database Initialization:**
   - Run the script once to create the necessary database and tables. Execute the following command in the terminal:
     ```bash
     python bank_system.py
     ```

3. **Dependencies:**
   - Make sure you have Python installed on your system.
   - Install the required Python packages using the following command:
     ```bash
     pip install mysql-connector-python
     ```

## Usage

1. **Run the Application:**
   - Execute the following command in the terminal to start the banking system application:
     ```bash
     python bank_system.py
     ```

2. **Sign In:**
   - Use the provided `E-mail` and `Password` to sign in.
   - For administrative access, sign in with the admin credentials.

3. **Banking Features:**
   - Once signed in, you can perform various banking operations such as transferring money, requesting money, and viewing account details.

## Features

- User authentication and authorization.
- Secure password storage.
- Transaction history tracking.
- Admin panel for managing user details.
- GUI implemented using Tkinter.

## Contributing

We welcome contributions from the community! If you're interested in contributing to this project, please follow these guidelines:

1. **Fork the Repository:**
   - Fork this repository to your own GitHub account.

2. **Clone the Repository:**
   - Clone the forked repository to your local machine using `git clone`.

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject


## License

This project is licensed under the [MIT License](LICENSE).

