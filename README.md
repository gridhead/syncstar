# SyncStar

Guest operated service for creating bootable USB storage devices at any community conference kiosk

## Screenshots

![](https://raw.githubusercontent.com/gridhead/syncstar/main/data/dash.png)

![](https://raw.githubusercontent.com/gridhead/syncstar/main/data/expo.png)

## Features

### For development
- Minimal command line interface based configuration with wide range of customizable options
- Stellar overall codebase quality is ensured with 100% coverage of functional backend code
- Over 34 checks are provided for unit based, end-to-end based integration based codebase testing
- GitHub Actions and Pre-Commit CI are enabled to automate maintenance of codebase quality

### For consumption
- Asynchronous multiprocessing allows for flashing multiple storage devices simultaneously
- Programming standards and engineering methodologies are maintained as much as possible
- Frontend is adaptive across various viewport types and browser-side assistive technologies
- Detailed documentation for both consumption and development purposes are readily provided

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

## Organization

1.  The images archive configuration file stores an unordered dictionary of images archives available for usage. 
    ```
    $ cat /etc/syncstar/images.yml
    ```

2.  The identifier for the images archives is the message digest text which can be found out using the following command.
    ```
    $ cat Fedora-Workstation-Live-x86_64-40-1.14.iso | sha256sum
    ```

3.  The second line per images archive entry stores the location of the file which is validated on every task run.
    ```
    path: /home/archdesk/Downloads/Fedora-Workstation-Live-x86_64-40-1.14.iso
    ```

4.  The third line per images archive entry stores the name that would be displayed to the users on the service frontend.
    ```
    name: Fedora Linux 40 Workstation rc1.14
    ```

5.  The fourth line per images archive entry stores the type that would be used for metadata generation purposes.
    ```
    type: fedora
    ```

6.  The images archive that have not been provided with one of the supported types would be provided with the generic type.
    ```
    type: common
    ```

7.  The images archive should be verified for their consistency by the service administrators before consumption.
    ```
    $ wget https://download.fedoraproject.org/pub/fedora/linux/releases/40/Workstation/x86_64/iso/Fedora-Workstation-40-1.14-x86_64-CHECKSUM
    ```

8.  The following types of images archive are supported for metadata generation purposes used on the service frontend.

    | #  | Name                     | Identity | Icon                                                                                                                                                   |
    |----|--------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
    | 1  | Android                  | `gdroid` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/9d52ca1ee37208482a05038d59664689d32f53f5189486932db8d6adbe481126.svg) |
    | 2  | Arch Linux               | `archlx` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/1c48b14227a7e1091e740a3df7174bbddc453917cc287e503315ae6f1a845b0e.svg) |
    | 3  | CentOS Stream            | `centos` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/87e960134335e7a8888b69331157a8a84215ed8dbb041ecd3ce73d3866d7f3d3.svg) |
    | 4  | Debian Linux             | `debian` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/f981aab3aaa188a7d289009af14600152c1ea28e9ad758ed4b97aa5620a74456.svg) |
    | 5  | Fedora Linux             | `fedora` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/e56f0c223307c5ebc30f78872f1887189715a2afd18c9e9204a63c03e781c271.svg) |
    | 6  | Kodi or XBMC             | `kodimc` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/2ad165fc2120ad592bdbf852fe501ddaad6e2b944bff7d945d127b4e73a1699e.svg) |
    | 7  | Linux Mint               | `lxmint` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/33f5c702ffcee2b326dec6d9e8b46730a8cf975a66fc0e5d84e674cacf41c3e4.svg) |
    | 8  | Manjaro Linux            | `mnjaro` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/246f21c66f18e728feb8e9ad0dd8f35b116656ddb519819e13798a579bdbc59a.svg) |
    | 9  | Red Hat Enterprise Linux | `redhat` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/170d2033c590e5e7b694ea5f7ae047fbf561768c78e30bf0f545f66e164ebc18.svg) |
    | 10 | OpenSUSE Linux           | `opsuse` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/e31d78dec9f573dac4e9fda28dd0d3357f4a3b7f5361f7be2498f223310f7254.svg) |
    | 11 | Ubuntu Linux             | `ubuntu` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/3b7f5a60779863249634141d594548e56208889dc32b783142cbf3999e8adbda.svg) |
    | 12 | Generic                  | `common` | ![](https://github.com/gridhead/syncstar/blob/main/syncstar/frontend/static/icon/fdf8c530789c78a450d5fae444905349afad1c6c257fb40b6a80de3fa7565c03.svg) |

## Appreciation

If you like the efforts made here and want to support the development of the project, please consider giving a star to 
the project and forking it your namespace. I appreciate all kinds of contributions - ranging from small sized bug fixes 
to major sized feature additions as well as from trivial documentation changes to awesome codebase refactoring. Even if 
you do not have the capacity to take the development for a spin, you can help me out by testing out the project and 
getting in touch with me on the issue tracker with the things that must be fixed and the things that should be introduced.
