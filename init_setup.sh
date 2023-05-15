echo [$(date)]: "START" 
echo [$(date)]: "creating env with python 3.8 version" 
conda create --prefix ./phish_predictor_env python=3.8 -y
echo [$(date)]: "activating the environment" 
source activate ./phish_predictor_env
echo [$(date)]: "installing the dev requirements" 
pip install -r requirements_dev.txt
echo [$(date)]: "END" 