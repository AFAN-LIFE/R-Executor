import os, json
from config import R_PATH
os.environ['R_HOME'] = R_PATH
from flask import Flask, request, jsonify
import rpy2
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.conversion import converter_ctx
from rpy2.robjects import default_converter, pandas2ri
print(rpy2.__version__)

app = Flask(__name__)

rms = importr('rms')

def convert_r_to_python(obj):
    """
    将 R 对象转换为 Python 对象（支持递归转换）
    """
    # 如果是向量（数值、字符、逻辑等），转换为 Python 列表
    if isinstance(obj, (ro.vectors.IntVector, ro.vectors.FloatVector, ro.vectors.StrVector, ro.vectors.BoolVector)):
        return list(obj)
    # 如果是数据框，转换为 Python 字典
    elif isinstance(obj, ro.vectors.DataFrame):
        with localconverter(default_converter + pandas2ri.converter):
            return {col: list(obj.rx2(col)) for col in obj.colnames}
    # 如果是列表，递归转换
    elif isinstance(obj, ro.vectors.ListVector):
        return {name: convert_r_to_python(value) for name, value in zip(obj.names, obj)}
    # 如果是矩阵，转换为嵌套列表
    elif isinstance(obj, ro.vectors.Matrix):
        return [list(row) for row in obj]
    # 其他类型（如单个值），直接返回
    else:
        return obj
@app.route('/r_execute', methods=['POST'])
def run_r_script():
    try:
        data = request.json
        r_code = data.get("code", "")
        result_var = data.get("result_var", "")
        if not r_code or not result_var:
            return jsonify({
                "status": "error",
                "message": "Missing required parameters: 'code' and 'result_var'",
                "data": None
            }), 400

        # 使用 localconverter 显式设置转换规则
        # 创建R环境
        r = ro.r
        # 手动设置上下文
        converter_ctx.set(default_converter)
        print(r_code, result_var)
        with localconverter(default_converter):
            # 执行 R 代码
            r(r_code)
            # 获取结果
            results = ro.globalenv[result_var]
        print(results, type(results))
        # 将 R 对象转换为 Python 对象
        python_results = convert_r_to_python(results)
        print(python_results)
        # 返回成功响应
        return jsonify({
            "status": "success",
            "message": "R code run success",
            "data": python_results  # 将 R 对象转换为 Python 列表
        }), 200
    except Exception as e:
        # 捕获所有异常并返回详细错误信息
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error occurred: {error_traceback}")
        return jsonify({
            "status": "error",
            "message": f"Server Internal Error: {str(e)}",
            "traceback": error_traceback,
            "data": None
        }), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=False, debug=True)