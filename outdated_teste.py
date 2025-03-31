import subprocess
import platform

def obterSerialPlacaMae():
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.check_output(
                "wmic baseboard get serialnumber", 
                shell=True, 
                stderr=subprocess.STDOUT, 
                universal_newlines=True
            )
            serial = result.strip().split("\n")[-1].strip()
        elif system == "Linux":
            result = subprocess.check_output(
                "sudo dmidecode -t baseboard | grep 'Serial Number'", 
                shell=True, 
                stderr=subprocess.STDOUT, 
                universal_newlines=True
            )
            serial = result.split(":")[-1].strip()
        else:
            raise Exception("Sistema operacional não suportado.")
        return serial
    except Exception as e:
        print(f"Erro ao obter número de série da placa-mãe: {e}")
        return None

serial = get_motherboard_serial()
print(f"Número de série da placa-mãe: {serial}")