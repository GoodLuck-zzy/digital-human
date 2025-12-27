# 基础镜像，使用官方 python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY ./app ./app
COPY ./database ./database
# 运行命令，启动 FastAPI，绑定 0.0.0.0 方便容器外访问
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

