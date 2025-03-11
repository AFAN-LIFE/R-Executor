import os
from config import R_PATH
os.environ['R_HOME'] = R_PATH  # R安装路径

from flask import Flask, request, jsonify
import rpy2
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import default_converter
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.conversion import converter_ctx
print(converter_ctx.get())
print(rpy2.__version__)

app = Flask(__name__)

rms = importr('rms')
# 手动设置上下文
converter_ctx.set(default_converter)
print(converter_ctx.get())

code = '''
x <- 1:10
result_list <- list(
    x = x
)
'''

result_var = 'result_list'

r_code = code
result_var = result_var

# 创建R环境
r = ro.r
# 使用 localconverter 显式设置转换规则
with localconverter(default_converter):
    # 执行 R 代码
    r(r_code)
    # 获取结果
    results = ro.globalenv[result_var]
    print(results)