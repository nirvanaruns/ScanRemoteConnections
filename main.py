import psutil
from ip2geotools.databases.noncommercial import DbIpCity
import time

def network_monitor():
    try:
        # Obtener la fecha y hora actual
        current_time = time.strftime("[%Y-%m-%d %H:%M]")

        # Obtener las conexiones de red de tipo 'inet'
        connections = psutil.net_connections(kind='inet')

        with open("log_de_accesos.txt", "a") as log_file:
            for conn in connections:
                # Comprobar si la conexión está "ESTABLECIDA" y no es local (127.0.0.1)
                if conn.status == "ESTABLISHED" and conn.raddr.ip != "127.0.0.1":
                    log_file.write(f"{current_time} -> Se encontró una conexión\n")
                    get_process_details(conn.pid, log_file)
                    log_file.write(f"{current_time} -> Escaneando detalles en el host remoto ({conn.raddr.ip})\n")
                    show_ip_details(conn.raddr.ip, log_file)

    except psutil.AccessDenied:
        print("Acceso denegado para obtener datos de red.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

def show_ip_details(ip, log_file):
    try:
        # Obtener información de geolocalización de la dirección IP
        res = DbIpCity.get(ip, api_key="free")
        log_file.write(f"Dirección IP: {res.ip_address}\n")
        log_file.write(f"Ubicación: {res.city}, {res.region}, {res.country}\n")
        log_file.write(f"Coordenadas: (Lat: {res.latitude}, Lng: {res.longitude})\n")
    except Exception as e:
        log_file.write(f"Ocurrió un error: {str(e)}\n")

def get_process_details(pid, log_file):
    try:
        # Obtener detalles del proceso
        process = psutil.Process(pid)
        log_file.write(f"[+] Nombre del Proceso: {process.name()}\n")
        log_file.write(f"[+] ID del Proceso: {pid}\n")
        log_file.write(f"[+] Estado del Proceso: {process.status()}\n")
    except psutil.NoSuchProcess:
        log_file.write(f"No se encontró ningún proceso con PID {pid}\n")
    except psutil.AccessDenied:
        log_file.write(f"Acceso denegado al proceso con PID {pid}\n")
    except Exception as e:
        log_file.write(f"Ocurrió un error: {str(e)}\n")

if __name__ == "__main":
    # Iniciar el monitoreo de la red
    network_monitor()
