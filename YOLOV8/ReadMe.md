Based on Python 3.11.6【3.10】也许也可以
pip install -r requirements.txt
如果你想用gpu去运行
将虚拟环境或本地Python文件夹下Lib/site-packages目录下有关torch的所有文件删除
或者运行
pip uninstall torch torchaudio torchvision               
再运行（这是cuda版本12.1以上的）
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
cuda11.8版本将cu121改为cu118再运行
