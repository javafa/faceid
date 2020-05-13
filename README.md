# Lightweight Face Recognition   

* Framework : Python 3.7 + , Pytorch 1.4.0, FastAPI 0.1.0   

## Install   

1. download and unzip or [git clone]   
   download this project and unzip   
   move the directory   
   `cd [project]`   

2. install anaconda 3.x

3. create virtual environment and activate   
   `conda create -n [project name] python=3.7`   
   `conda activate [project name]`   

4. (optional) download pre-trained   
   download latest model_mobilefacenet.pth to the [project] directory

5. (additional) for GPU version   
   install CUDA Toolkit   
   install cuDNN   
   
6. install Pytorch and Cuda   
   - GPU (nvidia product only)   
   `conda install pytorch torchvision cudatoolkit=10.1 -c pytorch`   
   (need to check your cuda version)   
   - CPU   
   `conda install pytorch torchvision cpuonly -c pytorch`
   
7. (additional) for windows > before install requirements
   install Microsoft Build Tools 2015 Update 3 for bcolz package   
   (visualcppbuildtools_full.exe)   

8. install requirement packages   
   `pip install -r requirements.txt`   
   (could not install some packages by conda install)   

## Run server   
   ```
   cd [project] directory
   python server.py
   ```

## Test in the web browser   
   - open chrome   
   http://127.0.0.1:8000/docs   
   
## copyright &copy; 2020 flow9.net   
   