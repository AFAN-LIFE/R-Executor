from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/python_run', methods=['POST'])
def run_r_script():
    data = request.json
    r_code = data.get("code", "")
    result_var = data.get("result_var", "")

    if not r_code or not result_var:
        return jsonify({"error": "Missing required parameters"}), 400

    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".R") as temp_r_script:
        temp_r_script.write(r_code.encode("utf-8"))
        temp_r_script.close()

        try:
            # 运行 R 代码
            command = f"Rscript {temp_r_script.name}"
            output = subprocess.run(command, shell=True, capture_output=True, text=True)

            # 解析结果
            if output.returncode == 0:
                result_command = f"Rscript -e 'print({result_var})'"
                result_output = subprocess.run(result_command, shell=True, capture_output=True, text=True)
                result = result_output.stdout.strip()
                return jsonify({"result": result})
            else:
                return jsonify({"error": output.stderr.strip()}), 500
        finally:
            os.remove(temp_r_script.name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
