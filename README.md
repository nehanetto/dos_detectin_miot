# dos_detectin_miot
Introduction: 
This Configuration Manual documents the complete technical setup used to develop, deploy, and evaluate the IoMT Intrusion Detection Framework combining Suricata IDS, a custom IoMT sensor simulation, packet capture, and machine-learning-based anomaly detection.

It details every step required to reproduce the environment across multiple virtual machines, including network configuration, software dependencies, sensor data generation, attack simulation, and ML pipeline execution.

The manual is structured to ensure that another researcher or examiner can fully rebuild the system from scratch without ambiguity.

Virtual Machine Setup:
Two Virtual Machines (VMs) were configured in VirtualBox to simulate a healthcare IoMT network:
	IDS VM
•	OS: Ubuntu 20.04 LTS
•	Tools Installed:
o	Suricata IDS
o	tshark / wireshark-cli
o	Python3, pip, scikit-learn, pandas
•	Assigned IP:

Captured using ip a

•	enp0s3: inet 192.168.0.245  
 Sensor VM
•	OS: Ubuntu 20.04 LTS
•	Tools Installed:
o	Python3
o	hping3 (for SYN flooding)
•	Assigned IP:
•	enp0s3: inet 192.168.0.29  
 Both VMs were bridged on the same network to simulate realistic IoMT communication.
Suricata Installation & Configuration (IDS VM)

Install Suricata

	sudo apt update
	sudo apt install suricata -y
Enable Real-Time Logging
Suricata logs stored at:
  /var/log/suricata/fast.log
To view logs in real time:

 	sudo tail -f /var/log/suricata/fast.log

 Restart Suricata

sudo systemctl restart suricata

IoMT Sensor Simulation (Sensor VM)
A custom Python script (iomt_sensor.py) was used to mimic heart-rate and blood-pressure transmission from a wearable medical device.

Run Sensor Script
python3 iomt_sensor.py
Output example (Figure included):
Sent: HeartRate:82, BP:118
Sent: HeartRate:78, BP:112
Sent: HeartRate:69, BP:121
...
This script generates continuous benign traffic to the IDS VM.

 
 Attack Simulation (Sensor VM)
To evaluate IDS behaviour under stress, a SYN-Flood attack was launched targeting the MQTT broker port (1883).

SYN Flood Command
		
		sudo hping3 -S --flood -p 1883 192.168.0.245
Output (included as Figure):
11207 packets transmitted, 0 received, 100% packet loss
Suricata triggered alerts immediately.

Suricata Alert Summary Script (IDS VM)
A custom Python script (alert_stats.py) was developed to parse Suricata logs and summarise alerts.

  Run Script
	
	sudo python3 alert_stats.py
Output (Figure for Experiment 3):
====== SURICATA ALERT SUMMARY ======
DoS Alerts (High SYN Rate): 6
Excessive Retransmission: 3
FIN Out-of-window Alerts: 2


Packet Capture & Feature Extraction
	 
	 Capture Packets
Using tshark:
sudo tshark -i enp0s3 -w capture.pcap
	
	Extract Features for ML
A custom extraction script converts PCAP to CSV:
Features extracted:
•	packet_size
•	src_ip
•	dst_ip
•	time_delta
	 Machine Learning Pipeline (IDS VM)
Models evaluated:
•	Support Vector Classifier (SVC)
•	Random Forest
•	k-Nearest Neighbour (k-NN)
	 Training Script: 
	  	
		train_models.py
Important components:
Load Dataset
df = pd.read_csv("iomt_dataset.csv")
Encode IPs

	le = LabelEncoder()
	df["src_ip"] = le.fit_transform(df["src_ip"].astype(str))
	df["dst_ip"] = le.fit_transform(df["dst_ip"].astype(str))
Feature Selection

	X = df[["packet_size","src_ip","dst_ip","time_delta"]]
	Y = df["label"]
Train/Test Split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
8.1.1	8.2 Results Summary Example (Figure)
accuracy       0.91
macro avg      0.87
weighted avg   0.91
ROC-AUC: 0.977
These results are included in Section 6.5 of the dissertation.
 
	Directory Structure
/project_root
│── iomt_sensor.py
│── alert_stats.py
│── train_models.py
│── capture.pcap
│── iomt_dataset.csv
│── suricata_rules/
│── README.md

Reproducibility Notes
 Ensure Both VMs Are Reachable
Use:
ping 192.168.0.245
ping 192.168.0.29
 Reset Suricata Logs Before Each Test

	sudo rm /var/log/suricata/fast.log
	sudo systemctl restart suricata
Keep Clocks in Sync
VM clock drift can distort time-delta features.

Troubleshooting
Issue	Cause	Fix
No Suricata alerts	Wrong port or rule disabled	Restart Suricata, check rules
Sensor script not sending	Firewall or wrong IP	Update destination IP
ML accuracy too low	Imbalanced dataset	Oversampling / feature tuning
pcap empty	Wrong interface	Run ip a to verify interface name

Conclusion
All configurations required to reproduce the full IDS pipeline—from IoMT sensor simulation to Suricata detection and machine-learning model evaluation. It enables examiners and researchers to validate system behaviour under both benign and attack conditions.
