# 直播图片匹配实验室

## 环境版本

- Python 3.12.10
- Windows PowerShell

## 启动虚拟环境

```powershell
cd E:\Project\livestream-image-matcher-lab
.\.venv\Scripts\Activate.ps1
```

## 安装依赖

先启动虚拟环境，然后执行：

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 运行测试

```powershell
python -m pytest
```

## 数据与 Git 约定

原始图片不进 Git。请将本地原始图片放在 `data/raw/` 下；原始图片、处理后的图片、生成的索引以及个人运行日志均已通过 `.gitignore` 忽略。只有安全且适合共享的少量测试样例可以放在 `data/sample/` 下。
