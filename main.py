import psutil
from ip2geotools.databases.noncommercial import DbIpCity
import time

# Un diccionario para realizar un seguimiento de la fecha y hora de inicio de cada proceso
proceso_inicio_tiempo = {}

def network_monitor():
    try:
        # Obtener la fecha y hora actual en formato "día/mes/año"
        current_time = time.strftime("[%d/%m/%Y %H:%M]")

        # Obtener las conexiones de red de tipo 'inet'
        connections = psutil.net_connections(kind='inet')

        with open("log_de_accesos.txt", "a", encoding="utf-8") as log_file:
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

def get_process_details(pid, log_file):
    try:
        # Obtener detalles del proceso
        process = psutil.Process(pid)
        proceso_nombre = process.name()

        # Obtener la fecha y hora de inicio del proceso
        proceso_inicio = time.strftime("[%d/%m/%Y %H:%M]", time.localtime(process.create_time()))

        # Calcular el tiempo de conexión actual
        tiempo_actual = time.time()
        tiempo_conexion = tiempo_actual - process.create_time()

        # Almacenar la fecha y hora de inicio del proceso en el diccionario
        proceso_inicio_tiempo[proceso_nombre] = proceso_inicio

        log_file.write(f"[+] Nombre del Proceso: {proceso_nombre}\n")
        log_file.write(f"[+] ID del Proceso: {pid}\n")
        log_file.write(f"[+] Estado del Proceso: {process.status()}\n")
        log_file.write(f"[+] Cantidad de veces detectado: {proceso_contador[proceso_nombre]}\n")  # Corrección aquí
        log_file.write(f"[+] Hora de inicio del proceso: {proceso_inicio}\n")
        log_file.write(f"[+] Tiempo de conexión actual: {tiempo_conexion} segundos\n")
    except psutil.NoSuchProcess:
        log_file.write(f"No se encontró ningún proceso con PID {pid}\n")
    except psutil.AccessDenied:
        log_file.write(f"Acceso denegado al proceso con PID {pid}\n")
    except Exception as e:
        log_file.write(f"Ocurrió un error: {str(e)}\n")

if __name__ == "__main":
    # Iniciar el monitoreo de la red
    network_monitor()
