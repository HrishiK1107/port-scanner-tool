import socket
import threading
import logging
import requests
from queue import Queue

# Set up logging
logging.basicConfig(filename='port_scanner.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Geolocation API URL
GEOLOCATION_API_URL = 'http://ip-api.com/json/{}'

# Port descriptions and vulnerability checks
PORT_DESCRIPTIONS = {
    21: ("FTP", "Open FTP port; check for anonymous login."),
    22: ("SSH", "Open SSH port; ensure strong authentication."),
    23: ("Telnet", "Insecure; consider using SSH instead."),
    25: ("SMTP", "Open SMTP port; verify for open relay."),
    53: ("DNS", "Check for DNS zone transfer vulnerabilities."),
    80: ("HTTP", "Check for common web vulnerabilities."),
    110: ("POP3", "Ensure secure access; check for weak passwords."),
    143: ("IMAP", "Ensure secure access; check for weak passwords."),
    443: ("HTTPS", "Check SSL/TLS configuration."),
    3306: ("MySQL", "Check for weak credentials."),
    8080: ("HTTP Alternate", "Check for common web vulnerabilities."),
}

# Function to grab banners
def grab_banner(ip, port):
    try:
        with socket.socket() as sock:
            sock.settimeout(2)
            sock.connect((ip, port))
            banner = sock.recv(1024).decode().strip()
            return banner
    except Exception as e:
        return None

# Function to get geolocation data, including city, country, ISP, and format as a Google Maps link
def get_geolocation(ip):
    try:
        response = requests.get(GEOLOCATION_API_URL.format(ip))
        data = response.json()
        if data['status'] == 'fail':
            return None  # Return None if geolocation fails
        
        city = data.get('city', 'Unknown City')
        country = data.get('country', 'Unknown Country')
        isp = data.get('isp', 'Unknown ISP')
        lat = data.get('lat', 0)
        lon = data.get('lon', 0)

        google_maps_link = f"https://www.google.com/maps/@{lat},{lon},15z"  # 15z is the zoom level
        
        # Construct and return geolocation information
        geolocation_info = {
            'city': city,
            'country': country,
            'isp': isp,
            'lat': lat,
            'lon': lon,
            'google_maps_link': google_maps_link
        }
        return geolocation_info
    except Exception as e:
        print(f"Could not get geolocation data: {e}")
        return None

# Function to scan ports and check for vulnerabilities
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            if result == 0:
                banner = grab_banner(ip, port)
                description, vulnerability = PORT_DESCRIPTIONS.get(port, ("Unknown Port", "No known vulnerabilities"))
                log_result(ip, port, description, banner, vulnerability)
            else:
                print(f"{ip}:{port} is closed.")
    except Exception as e:
        print(f"Error scanning {ip}:{port} - {e}")

# Function to log results
def log_result(ip, port, description, banner, vulnerability):
    if banner:
        logging.info(f"{ip}:{port} is open - {description} - Banner: {banner} - Vulnerability: {vulnerability}")
        print(f"{ip}:{port} is open - {description} - Banner: {banner} - Vulnerability: {vulnerability}")
    else:
        logging.info(f"{ip}:{port} is open - {description} - No banner - Vulnerability: {vulnerability}")
        print(f"{ip}:{port} is open - {description} - No banner - Vulnerability: {vulnerability}")

# Worker function for threading
def worker():
    while True:
        ip, port = queue.get()
        scan_port(ip, port)
        queue.task_done()

# Main function to initiate the scanner
def main(target_ip):
    global queue
    queue = Queue()
    
    # Start worker threads
    for _ in range(10):  # Adjust the number of threads as needed
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    # Predefined list of ports to scan
    ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]  # Add more ports as needed

    # Add ports to the queue
    for port in ports:
        queue.put((target_ip, port))

    queue.join()  # Wait for all tasks to complete

    # Get and log geolocation data after the port scanning is completed
    geo_data = get_geolocation(target_ip)
    if geo_data:
        print(f"\nGeolocation for {target_ip}:")
        print(f"City: {geo_data['city']}")
        print(f"Country: {geo_data['country']}")
        print(f"ISP: {geo_data['isp']}")
        print(f"Latitude: {geo_data['lat']}")
        print(f"Longitude: {geo_data['lon']}")
        print(f"Google Maps Link: {geo_data['google_maps_link']}")  # This will be a clickable link

        logging.info(f"Geolocation for {target_ip}: City - {geo_data['city']}, Country - {geo_data['country']}, ISP - {geo_data['isp']}")
        logging.info(f"Latitude: {geo_data['lat']}, Longitude: {geo_data['lon']}")
        logging.info(f"Google Maps Link: {geo_data['google_maps_link']}")
    else:
        print(f"Geolocation data could not be retrieved for {target_ip}.")
        logging.info(f"Geolocation data could not be retrieved for {target_ip}.")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    main(target_ip)
