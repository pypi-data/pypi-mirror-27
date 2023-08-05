Gitwebui
========

Gitwebui is a ihm for git repository

You can use gitwebui for local git repository or git server

Installation
------------

    pip install gitwebui
        
Or

    git clone https://github.com/fraoustin/gitwebui.git
    cd gitwebui
    python setup.py install

Usage
-----

Create quickly a server repository 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create a server repository for projet "test"

    docker run -d -e "GITPROJECT=test" -p 80:80 -v <your_path>:/var/lib/git/ fraoustin/gitweb

user default is gituser and password default is gitpassword

you can clone project

    git clone http://gituser:gitpassword@localhost/test.git

you can see on  http://localhost/test.git

Advanced
~~~~~~~~

You can change user and password by variable environment

    docker run -d -e "CONTAINER_TIMEZONE=Europe/Paris" -e "GITUSER=gituser" -e "GITPASSWORD=gitpassword" -e "GITPROJECT=test" --name test -p 80:80 -v /var/lib/git/:. fraoustin/gitweb


If you want add user, add project,... you can change 00_init.sh