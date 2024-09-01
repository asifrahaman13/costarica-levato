# How to run the application

![Screenshot from 2024-09-01 23-46-32](https://github.com/user-attachments/assets/51210771-fec3-4a8b-b036-0c2a73f25e48)
![Screenshot from 2024-09-01 23-45-50](https://github.com/user-attachments/assets/3bad5118-f177-4836-8942-5f83de33cba0)
![Screenshot from 2024-09-01 23-46-02](https://github.com/user-attachments/assets/05e92549-ac35-4735-ba83-290962668786)


First clone the repository

```bash
git clone https://github.com/asifrahaman13/costarica-levato
```

Create the virtual environement.

```bash
virtualenv .venv
source .venv/bin/activate
```

Next you can install the required packages and libraries.

```bash
pip install -r requirements.txt
```

Create a .env file from the .env.exmaple

```bash
cp .env.example .evn
```

Next enter the credential for the postgres database.

Now you can run the Jupyter notebooks using the virtual env kernel.
