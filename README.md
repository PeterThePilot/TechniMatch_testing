# TechnimatchApp
# Installation
1. Open a new empty project in your IDE of choise.

2. Download the repository using the following command in the terminal:
```bash
git clone https://github.com/PeterThePilot/TechniMatch_testing.git
```
3. Change directory in the Terminal:
```bash
cd .\TechniMatch_testing\
```
4. Run the following command in the terminal:
```bash
conda env create -f environment.yml 
```
5. Activate the enviroment either in terminal or in IDE. 
```bash
conda activate IIS_venv
```
# Running the Application
After the env is configured enter your google api key to the following path:(open this file and replace the empty string with the key string)
```bash
TechniMatch_testing\users\env.py
```
You can get your api key for free :
```bash
https://ai.google.dev/tutorials/setup 
```
Now save all the files.

Open the terminal and run the command:
```bash
python manage.py runserver
```
You will get a message with the link to the website.
```bash
http://127.0.0.1:8000/
```
Thank you.
