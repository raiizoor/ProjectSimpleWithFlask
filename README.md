

<h1>Web Developer Creating CRUD :construction_worker:</h1>

Simple project where created CRUD using **Python** with framework **Flask**.

_**Tools used**_ :hammer_and_wrench:

* Python 3
* Flask
* Flask-mysqldb
* JavaScript 
* Jquery
* Bootstrap
* Bulma


<h1> How Running Project your System :rocket:</h1> 

1. First shall create environment python using command.
```powershell
    python -m venv .venv
```

2. Install [Mysql Server](https://dev.mysql.com/downloads/installer/). Active your environment virtual and install [Mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient) using pip.

![!image](ImagesAndGif-forProject/PythonExtension.png) 

```powershell
    (.venv) pip install .\mysqlclient-1.4.6-cp39-cp39-win_amd64.whl
```

3. Next you shall to give command in your enmviroment. To install packages from flask. Needed to run the application :construction_worker:
```powershell
    make install
```
-  Had sure you have install **make** in environment S.O, if you don't have excute this commmand
```powershell
    pip install -r requirements.txt
```


4. Run prepara_banco.py - will create db

5. Run jogoteca.py - finish!!! :rocket: Now your system is runing

6. You can loggin using **luan** for login and **flask** for senha.

7. List with user you find in archive **prepara_banco**
   
Screen the Login, list from Games and list from Users.

<h1>Aplication :computer:</h1>

Login:  :woman_technologist:
![!image](ImagesAndGif-forProject/ScreenLogin.png)

List Games: :bookmark_tabs: :video_game: 
![!image](ImagesAndGif-forProject/ListGames.png)

List Users: :bookmark_tabs: :mage:
![!image](ImagesAndGif-forProject/ListUsers.png)

How add game in games list: :bookmark_tabs: :man_technologist:
![](ImagesAndGif-forProject/AddGameInList.gif)

<h2> Next Steps :gear:</h2>

Add picture from user in Header, when is logged.

Fix the login screen bug.

Add in table user one field for user admin, and user standard.





