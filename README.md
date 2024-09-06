## Purpose
To learn more about DoS/related attacks, I:
1. built a socket-level web-server, hosting some demo applications.
2. developed various DoS/DDoS/etc attacks to successfully attack the server
3. Implemented security mechaisms to protect the server against such attacks

A documentation of my notes / research is available in report.pdf above.

## Screenshots

Server working as expected:
<img width="400" alt="Screenshot 2024-09-06 at 5 43 48 pm" src="https://github.com/user-attachments/assets/01aba2c2-9c9e-42b7-abdf-f4794440727d">

Example client website, hosted on server (there are a few, in the /client_websites directory:
<img width="300" alt="Screenshot 2024-09-06 at 5 58 46 pm" src="https://github.com/user-attachments/assets/577d9f63-872c-4140-aecb-3783d9c9cd06">


Effect of attacks on server:
<img width="900" alt="Screenshot 2024-09-06 at 5 45 22 pm" src="https://github.com/user-attachments/assets/da803961-e8ad-4696-a6cf-584a72b21913">

Effect of attacks after server fortifications: 
<img width="936" alt="Screenshot 2024-09-06 at 5 46 03 pm" src="https://github.com/user-attachments/assets/6d2b924f-e9ce-4330-9443-f93fd90e3ad9">



## How to Run
1. to start web server, naavigate to /iteration1 (or /iteration2 for fortified), run `python3 web_server.py`.
2. to run a client website on the running server, on a browser visit the url of format: `server_URL:port/client_website_dir_name`. e.g. `http://127.0.0.1:8080/messagingSite`
3. to run various attacks, open another terminal window, navigate to /attacker directory, run of format: `python3 ATTACK_NAME.py`.
