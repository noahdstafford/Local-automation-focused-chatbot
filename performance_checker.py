# Essentially the Windows Task Manager packed into a Python toolkit.
import psutil
from chat import ask_ollama

# Create function to check performance and give a detialed responds to the user 
def run_performance_checker():
    # Checks the computers brain (CPU) is currently working 
    CPU_performance = psutil.cpu_percent()
    # Looks at the RAM of the PC and checks how its currently being used
    Virtual_memory = psutil.virtual_memory()
    # Scans your physical harddrive to check your long term storage capacity
    Disk_space = psutil.disk_usage("C:\\")

    prompt = f"""You are a techinal analyser of a PC based off the following documents i give and give me an industrial level analysis of the performance aspects 
    of the this PC and give clear pointers of the failings of the PC if applicable and comment clearly on the positives of the current PC's performance while also
    giving suggestions for stronger/ more reliable

    Performance statistics:
    CPU performance {CPU_performance}.
    Memory performance: {Virtual_memory.percent}% used, {Virtual_memory.available / (1024**3)} GB available, {Virtual_memory.total / (1024**3)} GB total.
    Disk performance: {Disk_space.percent}% used, {Disk_space.free / (1024**3)} GB free, {Disk_space.total / (1024**3)} GB total."""

    # Sends the message to ollama to have a look 
    Computer_performance = ask_ollama(prompt)
    return Computer_performance

if __name__ == "__main__":
    result = run_performance_checker()
    print(result)