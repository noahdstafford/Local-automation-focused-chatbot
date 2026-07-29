import psutil
from chat import ask_ollama
                               
def run_performance_checker():
    CPU_performance = psutil.cpu_percent()
    Virtual_memory = psutil.virtual_memory()
    Disk_space = psutil.disk_usage("C:\\")

    print(Virtual_memory)
    print(Disk_space)

    prompt = f"""You are a techinal analyser of a PC based off the following documents i give and give me an industrial level analysis of the performance aspects 
    of the this PC and give clear pointers of the failings of the PC if applicable and comment clearly on the positives of the current PC's performance.

    Performance statistics:
    CPU performance {CPU_performance}. Memory performance {Virtual_memory}. Disk performance {Disk_space}."""

    # Sends the message to ollama to have a look 
    Computer_performance = ask_ollama(prompt)
    return Computer_performance

result = run_performance_checker()
print(result)