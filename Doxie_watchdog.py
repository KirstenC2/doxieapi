import os
from doxieapi import DoxieScanner
import re
import time

def download_scans(scanner, save_directory):
    return scanner.download_scans(save_directory)

def check_and_download_scans(scanner, save_directory, no_scan_count):
    print("Checking for new scans...")
    
    existing_files = os.listdir(save_directory)
    
    if len(existing_files) != len(scanner.scans):
        print("Found new scans...!")
        # Reset no_scan_count if new scans are found
        no_scan_count = 0
        # Get the last scan number
        filename = existing_files[-1]
        numbers_only = re.findall(r'\d+', filename)
        last_scan_number = numbers_only[0]
        
        for i in range(int(last_scan_number) + 1, len(scanner.scans) + 1):
            next_scan_number = str(i).zfill(4)
            scans_filename = f"IMG_{next_scan_number}.JPG"
            print(f"Downloading {scans_filename}...")
            scanner.download_scan(f"/DOXIE/JPEG/{scans_filename}", save_directory)
    else:
        print("No new scans")
        no_scan_count += 1
        return no_scan_count

def monitor_scans(scanner, save_directory, interval=100, max_no_scan_attempts=3):
    no_scan_count = 0
    while no_scan_count < max_no_scan_attempts:
        no_scan_count = check_and_download_scans(scanner, save_directory, no_scan_count)
        time.sleep(interval)

def main():
    print("Discovering any scanners...")
    scanners = DoxieScanner.discover()

    if len(scanners) != 0:
        print("Scanner connected: ", scanners)
        save_directory = r"C:\Users\User\Desktop\Freelance\Pic"
        scanner = scanners[0]
        
        monitor_scans(scanner, save_directory)
    else:
        print("No scanner is connected")

if __name__ == "__main__":
    main()
