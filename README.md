# SyncStar

Create bootable USB drives at the convenience of any headless device

## Installation

### For development

1.  Install the supported version of Python, Virtualenv, Poetry, Redis and CoreUtils on your Fedora Linux installation.
    ```
    $ sudo dnf install python3 python3-virtualenv poetry
    ```
    ```
    $ sudo dnf install redis coreutils
    ```

2.  Clone the repository to your local storage and make it your present working directory.
    ```
    $ git clone https://github.com/gridhead/syncstar.git
    ```
    ```
    $ cd syncstar
    ```

3.  Establish a virtual environment within the project and activate it for installing dependencies.
    ```
    $ virtualenv venv
    ```
    ```
    $ source venv/bin/activate
    ```

4.  Check the validity of the project configuration and install the dependencies from the lockfile.
    ```
    (venv) $ poetry check
    ```
    ```
    (venv) $ poetry install
    ```

### For consumption

1.  Install the supported version of Python, Python Package Installer Redis CoreUtils on your Fedora Linux installation.
    ```
    $ sudo dnf install python3 python3-pip
    ```
    ```
    $ sudo dnf install redis coreutils
    ```

2.  Elevate the privileges to the superuser level and install the `syncstar` package from Python Package Index.
    ```
    $ sudo -s
    ```
    ```
    # pip3 install syncstar
    ```

3.  Configure the service unit files for the endpoint service and worker service to the system services directory.
    ```
    $ sudo wget https://raw.githubusercontent.com/gridhead/syncstar/main/syncstar/system/endpoint.service -O /etc/systemd/system/ss-endpoint.service
    ```
    ```
    $ sudo wget https://raw.githubusercontent.com/gridhead/syncstar/main/syncstar/system/worker.service -O /etc/systemd/system/ss-worker.service
    ```

4.  Enable the service unis for the endpoint service and worker services.
    ```
    $ sudo systemctl enable ss-endpoint.service
    ```
    ```
    $ sudo systemctl enable ss-worker.service
    ```

## Initialization

1.  Download the Fedora Linux live images to a certain directory and make the images archive configuration file.
    ```
    $ wget https://download.fedoraproject.org/pub/fedora/linux/releases/40/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-40-1.14.iso
    ```
    ```
    $ cp Fedora-Workstation-Live-x86_64-40-1.14.iso /etc/syncstar/images/Fedora-Workstation-Live-x86_64-40-1.14.iso
    ```

2.  Download the images archive configuration file and make changes to include the recently downloaded image files.
    ```
    $ wget https://raw.githubusercontent.com/gridhead/syncstar/main/syncstar/config/images.yml -O /etc/syncstar/images.yml
    ```
    ```
    $ nano /etc/syncstar/images.yml
    ```

3.  Set the value of the following environment variable as the present location of the images archive configuration file.
    ```
    $ nano /home/$(whoami)/.bashrc
    ```
    ```
    $ export SYNCSTAR_ISOSYAML=/etc/syncstar/images.yml
    ```

4.  Enable the Redis service unit and check the status of the service.
    ```
    $ sudo systemctl enable redis.service
    ```
    ```
    $ sudo systemctl status redis.service
    ```

## Execution

### For development

1.  Ensure that the Redis service unit is active and check the status of the service.
    ```
    $ sudo systemctl start redis.service
    ```
    ```
    $ sudo systemctl status redis.service
    ```

2.  In a separate terminal session, execute the following command to start the endpoint service in an activated virtual environment.
    ```
    $ source venv/bin/activate
    ```
    ```
    (venv) $ syncstar --port 8080 --repair false --period 2 --images $SYNCSTAR_ISOSYAML
    ```
     - This will start the endpoint service on port 8080 available across all network interfaces of the host device.  
     - The debug mode for the endpoint service will be disabled and the information would be refreshed after 2 seconds.  
     - The images archive configuration file mentioned previously will be used as a source for the live images.  
     - Dictionaries consisting of task schedules will not persist after a live reload when using the debug mode.

3.  In a separate terminal session, execute the following command to start the worker service in an activated virtual environment
    ```
    $ source venv/bin/activate
    ```
    ```
    (venv) $ sudo SYNCSTAR_ISOSYAML=/etc/syncstar/images.yml celery -A syncstar.task.taskmgmt worker --loglevel=info
    ```  
     - This will start the worker service that would accept tasks requested by the users of the endpoint service.  
     - The debug mode for the worker service will be disabled and there will be a default concurrency of 12 processes.  
     - The images archive configuration file mentioned previously will be used as a source for the live images.  
     - Dictionaries consisting of task schedules will not persist after a live reload when using the debug mode.

4.  Visit the homepage of the endpoint service using the browser of your choice to get started with using SyncStar.

### For consumption

1.  Ensure that the Redis service unit is active and check the status of the service.
    ```
    $ sudo systemctl start redis.service
    ```
    ```
    $ sudo systemctl status redis.service
    ```

2.  Start the endppint service unit and check the status of the service.
    ```
    $ sudo systemctl start ss-endpoint.service
    ```
    ```
    $ sudo systemctl status ss-endpoint.service
    ```

3.  Start the worker service unit and check the status of the service.
    ```
    $ sudo systemctl start ss-worker.service
    ```
    ```
    $ sudo systemctl status ss-worker.service
    ```

4.  Visit the homepage of the endpoint service using the browser of your choice to get started with using SyncStar.

## Appreciation

If you like the efforts made here and want to support the development of the project, please consider giving a star to 
the project and forking it your namespace. I appreciate all kinds of contributions - ranging from small sized bug fixes 
to major sized feature additions as well as from trivial documentation changes to awesome codebase refactoring. Even if 
you do not have the capacity to take the development for a spin, you can help me out by testing out the project and 
getting in touch with me on the issue tracker with the things that must be fixed and the things that should be introduced.
