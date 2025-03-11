import requests
from config import URL
code = '''
# 读取数据
result_list <- list(
  vector = c(1, 2, 3),
  dataframe = data.frame(a = c(1, 2), b = c("x", "y")),
  matrix = matrix(1:4, nrow = 2)
)
'''

result_var = 'result_list'
data = {'code': code, 'result_var': result_var}
res = requests.post(URL, json=data)
print(res.text)