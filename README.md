# Advanced Port Scanner with Geolocation and Vulnerability Detection🛡️

This is an advanced Python-based port scanner that not only scans for open ports but also retrieves geolocation data for the target IP. It includes features like banner grabbing, vulnerability suggestions for open ports, and geolocation reporting with a Google Maps link. It is a useful tool for network administrators, penetration testers, and cybersecurity professionals.

### Features

- **Multithreaded Port Scanning:** Scans multiple ports simultaneously using multithreading for faster performance.
- **Banner Grabbing:** Attempts to retrieve banners from open ports for deeper analysis of the services running.
- **Vulnerability Suggestions:** Provides suggestions for potential vulnerabilities for common ports based on known security concerns.
- **Geolocation Information:** Fetches the target's city, country, ISP, latitude, and longitude, and generates a clickable Google Maps link to visualize the IP's location.
- **Logging:** All results, including open ports, banners, vulnerabilities, and geolocation data, are logged into `port_scanner.log` for future reference.

### Requirements

- **Python 3.x**
- Required Python libraries:
  - `socket`
  - `requests`
  - `threading`
  - `queue`
  - `logging`

You can install `requests` using the following command:

```bash
pip install requests
```

Run the script using this command:
```bash
python port_scanner.py
```
Example:
```bash
192.168.1.1:80 is open - HTTP - Banner: Apache HTTPD - Vulnerability: Check for common web vulnerabilities.
192.168.1.1:443 is open - HTTPS - No banner - Vulnerability: Check SSL/TLS configuration.

Geolocation for 192.168.1.1:
City: Pune
Country: India
ISP: ABC Internet Pvt. Ltd.
Latitude: 18.5204
Longitude: 73.8567
Google Maps Link: https://www.google.com/maps/@18.5204,73.8567,15z
```

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Disclaimer:
This tool is for **educational purposes only**. Unauthorized use of keylogging software may be illegal. Ensure that you have proper permission before using this tool.
