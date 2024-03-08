from flask import Flask, jsonify, render_template
import psutil
from nvitop import Device
import time
from flask_httpauth import HTTPBasicAuth

# 使用全局变量而不是 g 对象
last_net_io = psutil.net_io_counters()
last_time = time.time()

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "1234": "1234",  # 这里可以设置用户名和密码，建议在实际应用中使用更安全的存储方式
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')

@app.route('/data')
@auth.login_required
def data():
    global last_net_io, last_time  # 声明全局变量，以便更新它们
    now = time.time()
    current_net_io = psutil.net_io_counters()

    time_interval = max(now - last_time, 1)  # Prevent division by zero

    # Calculate upload and download rates in MB/s
    upload_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_interval / (1024 ** 2)
    download_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_interval / (1024 ** 2)

    # Update the global variables for next calculation
    last_net_io = current_net_io
    last_time = now

    cpu_usage = psutil.cpu_percent(percpu=True)
    memory = psutil.virtual_memory()
    gpu_infos = [
        {
            "name": str(device),
            "fan_speed": device.fan_speed(),
            "temperature": device.temperature(),
            "gpu_utilization": device.gpu_utilization(),
            "memory_total": device.memory_total(),
            "memory_used": device.memory_used(),
            "memory_free": device.memory_free(),
            "memory_used_gb": device.memory_used() / (1024 ** 3),
            "memory_total_gb": device.memory_total() / (1024 ** 3),
        }
        for device in Device.cuda.all()
    ]
    
    return jsonify(cpu_usage=cpu_usage, memory=memory._asdict(), gpu_infos=gpu_infos, upload_speed=upload_speed, download_speed=download_speed)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=14120, debug=True, extra_files=['index.html'])
