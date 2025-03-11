import json
import requests
from config import URL

code = '''
Sys.setlocale("LC_ALL", "en_US.UTF-8")  # 设置R的字符编码为UTF-8
library(rms)
r_df <- read.csv("train.csv")
# 验证数据格式
print(class(r_df))  # 应显示"data.frame"
print(colnames(r_df))  # 检查列名

# 构建模型（注意使用正确的数据对象）
model <- lrm(Heart_Disease ~ ., data = r_df)

# 生成预测概率
probabilities <- predict(model, type="fitted")

# 计算分类结果和准确率
predicted_class <- ifelse(probabilities > 0.5, 1, 0)
accuracy <- mean(predicted_class == r_df$Heart_Disease, na.rm=TRUE)

# 保存结果到R环境
result_list <- list(
    model_summary = capture.output(print(model)),
    accuracy = accuracy
)
'''

result_var = 'result_list'
data = {'code': code, 'result_var': result_var}
res = requests.post(URL, json=data)
print(res.text)