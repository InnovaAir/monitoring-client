import subprocess        
especificacao = subprocess.check_output('wmic nic get Manufacturer, Name, Description', shell=True, text=True)
especificacao = especificacao.strip().replace(" ", "").split("\n")[2]
print(especificacao)