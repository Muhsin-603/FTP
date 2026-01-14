---
THE VAULT // LOCAL EXCHANGE PROTOCOL

  _   _   _____   _   _   _       _____ 
 | | | | |  _  | | | | | | |     |_   _|
 | | | | | |_| | | | | | | |       | |  
 \ \ / / |  _  | | |_| | | |___    | |  
  \___/  |_| |_| \___/  |_____|    |_|  
                                        
  >> SYSTEM READY.
  >> WAITING FOR CONNECTION...

------------------------------------------------------------

MISSION BRIEFING

The Vault is a lightweight, self-hosted file exchange system designed for
local networks. It creates a secure, air-gapped environment where users
can transfer data between devices without relying on the cloud, internet,
or third-party surveillance.

Built with Flask, it turns any directory on your machine into a fully
interactive Cyber-Deck accessible via any web browser on your WiFi.

Fast. Private. Local. No nonsense.

------------------------------------------------------------

SYSTEM CAPABILITIES

- Terminal Aesthetics
  CRT-style interface with dark mode, monospace typography, glow effects,
  and scanlines.

- Secure Authentication
  User registration and login protected using password hashing (scrypt).

- Dynamic Navigation
  Browse folders and subdirectories directly from the browser.

- Deep Storage Injection
  Drag-and-drop entire folders while preserving directory structure.

- Incineration Protocols
  - Targeted Delete: Remove individual files or folders.
  - Purge Sector: Wipe the active directory with safety confirmation.

- Cross-Platform Access
  Works on phones, tablets, laptops, desktops. Browser is the only
  requirement.

------------------------------------------------------------

THREAT MODEL

Designed for:
  ✔ Local networks
  ✔ Trusted devices
  ✔ Air-gapped transfers
  ✔ Zero cloud dependency

Not designed for:
  ✘ Public internet exposure
  ✘ Anonymous access
  ✘ Hostile networks
  ✘ Production deployment

------------------------------------------------------------

OPERATOR FLOW

1. Launch the server.
2. Open the dashboard from any device on the network.
3. Authenticate.
4. Upload or manage files and folders.
5. Browse and organize content.
6. Purge when the mission ends.

------------------------------------------------------------

DEPLOYMENT INSTRUCTIONS

Pre-Requisites:
- Python 3.x installed.

Initialization:
- Clone the repository:
    git clone https://github.com/yourusername/the-vault.git
    cd the-vault

- Install dependencies:
    pip install flask

Launch Sequence:
- Default directory:
    python app.py

- Custom directory:
    python app.py "C:\Users\Drac\Documents\SecretProjects"
    python app.py /home/drac/secret_projects

------------------------------------------------------------

ESTABLISHING THE LINK

Server runs on port 5000.

Host Machine:
  http://localhost:5000

Other Devices:
- Find local IP:
    Windows: ipconfig
    Mac/Linux: ifconfig OR ip a

- Open in browser:
    http://192.168.1.15:5000

------------------------------------------------------------

OPERATIONAL SECURITY

- Secret Key
  Change app.secret_key in app.py before using on shared networks.

- Debug Mode
  Disable debug=True before real usage. Never expose publicly.

------------------------------------------------------------

CREDITS

Operator: Drac
System Architect: Jenny (AI Creative Partner)

> END OF TRANSMISSION.
...
