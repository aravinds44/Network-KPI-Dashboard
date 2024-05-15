import psycopg2
import random
import time
from faker import Faker
from collections import defaultdict

# PostgreSQL database connection parameters
DB_HOST = 'localhost'
DB_PORT = '8888'  # Default PostgreSQL port
DB_NAME = 'net_kpi'
DB_USER = 'admin'
DB_PASSWORD = 'admin'

# List of 24 states in India
STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal"
]

# Establish connection to PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Function to create table if not exists
def create_table_if_not_exists():
    conn = connect_to_db()
    cursor = conn.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS network_kpis (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            state TEXT,
            throughput_mbps FLOAT,
            latency_ms FLOAT,
            packet_loss_rate FLOAT,
            network_errors INTEGER,
            bandwidth_utilization_percent FLOAT,
            network_availability_percent FLOAT,
            jitter_ms FLOAT,
            mos FLOAT,
            http_traffic_packets FLOAT,
            udp_traffic_packets FLOAT,
            security_events_count INTEGER,
            connection_errors INTEGER,
            response_time_ms FLOAT
        )
    """

    cursor.execute(create_table_query)
    conn.commit()

    print("Table 'network_kpis' created successfully (if it didn't exist)")

    cursor.close()
    conn.close()

# Function to generate simulated network data
def generate_network_data():
    fake = Faker()
    conn = connect_to_db()
    cursor = conn.cursor()

    kpi_data = defaultdict(list)

    while True:
        # Create table if not exists
        create_table_if_not_exists()

        for state in STATES:
            # Simulate throughput (Mbps)
            throughput = random.uniform(100, 1000)  # random value between 100 and 1000 Mbps

            # Simulate latency (ms)
            latency = random.uniform(10, 50)  # random value between 10 and 50 ms

            # Simulate packet loss rate (%)
            packet_loss_rate = random.uniform(0.1, 5.0)  # random value between 0.1% and 5.0%

            # Simulate network errors
            network_errors = random.randint(0, 100)  # random number of errors

            # Simulate bandwidth utilization (%)
            bandwidth_utilization = random.uniform(20, 80)  # random value between 20% and 80%

            # Simulate network availability (%)
            network_availability = random.uniform(95, 100)  # random value between 95% and 100%

            # Simulate quality of service (QoS) metrics
            jitter = random.uniform(1, 10)  # random value between 1 and 10 ms
            mos = random.uniform(3, 5)  # random value between 3 and 5 (MOS scale for VoIP)

            # Simulate traffic patterns
            http_traffic = random.uniform(1000, 5000)  # random value between 1000 and 5000 packets
            udp_traffic = random.uniform(500, 2000)  # random value between 500 and 2000 packets

            # Simulate security events
            security_events = random.randint(0, 10)  # random number of security events

            # Simulate connection errors
            connection_errors = random.randint(0, 50)  # random number of connection errors

            # Simulate response time (ms)
            response_time = random.uniform(100, 500)  # random value between 100 and 500 ms

            # Store simulated data in a dictionary
            kpi_data[state].append((
                throughput,
                latency,
                packet_loss_rate,
                network_errors,
                bandwidth_utilization,
                network_availability,
                jitter,
                mos,
                http_traffic,
                udp_traffic,
                security_events,
                connection_errors,
                response_time
            ))

        # Insert simulated data into PostgreSQL table
        for state, data_list in kpi_data.items():
            for data_tuple in data_list:
                insert_query = """
                    INSERT INTO network_kpis (
                        state,
                        throughput_mbps,
                        latency_ms,
                        packet_loss_rate,
                        network_errors,
                        bandwidth_utilization_percent,
                        network_availability_percent,
                        jitter_ms,
                        mos,
                        http_traffic_packets,
                        udp_traffic_packets,
                        security_events_count,
                        connection_errors,
                        response_time_ms
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    state,
                    data_tuple[0],
                    data_tuple[1],
                    data_tuple[2],
                    data_tuple[3],
                    data_tuple[4],
                    data_tuple[5],
                    data_tuple[6],
                    data_tuple[7],
                    data_tuple[8],
                    data_tuple[9],
                    data_tuple[10],
                    data_tuple[11],
                    data_tuple[12]
                ))
            kpi_data[state] = []

        conn.commit()
        print(f"Simulated data inserted for all states.")

        time.sleep(3)  # sleep for 5 minutes (adjust as needed)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    generate_network_data()