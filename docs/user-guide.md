# User guide
This guide provides rules and examples on how to get started with AutoML Dashboard!

## Setting up the project

This guide was created using Windows, if you use other operating system please fill free to contribute to this guide.

### Step 1 Clone the repository

``` bash
git clone https://github.com/Niebowziemii/automl-dashboard.git
```

### Step 2 Download the data

Enter the following link:
[HERE] (https://www.kaggle.com/c/m5-forecasting-accuracy/data)

Authorize yourself and click the "download all" button to obtain the zip package:

![image](https://github.com/Niebowziemii/automl-dashboard/assets/59135705/3cc9a056-ac3a-4ac5-93a8-f9f671bc69c7)

Extract the downloaded folder in the root of the project and change the name of the folder to `input`

![image](https://github.com/Niebowziemii/automl-dashboard/assets/59135705/7e8ecd4e-526c-4d70-b0a8-4f966dd823a4)

```
automl-dashboard
├── input
│   └── m5-forecasting-accuracy
│       ├── calendar.csv
│       ├── sales_train_evaluation.csv
│       ├── sales_train_validation.csv
│       ├── sample_submission.csv
│       └── sell_prices.csv
...
```

### Step 3 Prepare the environment
This guide was created using `python == 3.10.11` and PowerShell
```
PS C:\...\automl-dashboard> python --version
Python 3.10.11
```

Install the package manager in your python (globally or if you use pyenv then only for the selected version)
```
pip install pipenv
```

Now check if everything works fine
```
PS C:\...\automl-dashboard> pipenv --version
pipenv, version 2023.7.11
```

Use the package manager to install the packages required to run the code:
```
PS C:\...\automl-dashboard> pipenv install --dev
Creating a virtualenv for this project...
Pipfile: C:\...\automl-dashboard\Pipfile
Using c:/users/<user>/.pyenv/pyenv-win/versions/3.10.11/python3.exe (3.10.11) to create virtualenv...
[ ===] Creating virtual environment...created virtual environment CPython3.10.11.final.0-64 in 1266ms
  creator CPython3Windows(dest=C:\Users\<user>\.virtualenvs\automl-dashboard-RpLtEANu, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=C:\Users\<user>\AppData\Local\pypa\virtualenv)
    added seed packages: pip==23.3.1, setuptools==69.0.2, wheel==0.41.3
  activators BashActivator,BatchActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

Successfully created virtual environment!
Virtualenv location: C:\Users\<user>\.virtualenvs\automl-dashboard-RpLtEANu
Installing dependencies from Pipfile.lock (171210)...
Installing dependencies from Pipfile.lock (171210)...
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```
### Step 4 Run the main

```
PS C:\...\automl-dashboard> pipenv run streamlit run main.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.16:8501

```
Click the link and enjoy!
