import os
import subprocess
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

# --- CONFIGURATION ---
# Laptop ka IP aur Port (Check kar lena aapka yahi hai)
host_ip = "http://10.48.56.178:11434"

# Model selection - DeepSeek is smarter for tools
# Agar Gemma use karna hai to "gemma3:1b" likh sakte ho
model_name = "deepseek-r1:8b"

llm = OllamaLLM(
    base_url=host_ip,
    model=model_name,
    temperature=0  # Temperature 0 matlab model seedhi baat karega, bakwas nahi
)

# --- SYSTEM TOOL ---
def get_linux_stats(query):
    """Actual Linux commands to get server health"""
    try:
        # Disk usage of root partition
        disk = subprocess.check_output("df -h / | awk 'NR==2 {print $5}'", shell=True).decode().strip()
        # System uptime
        uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()
        # Free memory in MB
        mem = subprocess.check_output("free -m | awk 'NR==2 {print $4}'", shell=True).decode().strip()
        
        return f"Uptime: {uptime}, Disk Usage: {disk}, Free Memory: {mem}MB."
    except Exception as e:
        return f"Error executing commands: {str(e)}"
#--- File SIZE ANALYSIS ---
def analyze_opt(query):
    try:
        # /opt ke andar top 5 sabse badi files/folders dhoondna
        analysis = subprocess.check_output("du -sh /opt/* 2>/dev/null | sort -rh | head -5", shell=True).decode().strip()
        return f"Top Space Consumers in /opt:\n{analysis}"
    except Exception as e:
        return f"Analysis Error: {str(e)}"
# Tool registration
linux_tool = Tool(
    name="monitor",
    func=get_linux_stats,
    description="Useful for checking server disk, uptime, and memory. Input should be 'status'."
)

# --- AGENT SETUP ---
agent = initialize_agent(
    [linux_tool], 
    llm, 
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,           # Taaki loop 3 baar se zyada na chale
    early_stopping_method="generate" # Loop rukne par last data dikhaye
)

# --- EXECUTION ---
if __name__ == "__main__":
    print(f"--- RHEL Agent connected ---")
    
    # Humne prompt mein format fixed kar diya hai
    query = """
    Check the server health using 'monitor' tool. 
    After you get the data, you MUST provide a response in this EXACT format:
    
    Thought: I have the data now.
    Final Answer: [Summarize Uptime, Disk, and Memory here]
    
    Now, start your work.
    """
    
    try:
        agent.invoke({"input": query})
    except Exception as e:
        # Agar phir bhi parse error aaye, toh output manually print karne ke liye
        print(f"\n--- System Status (Manual View) ---")
        print("Note: Agent data nikal chuka hai, bas format error hai.")
