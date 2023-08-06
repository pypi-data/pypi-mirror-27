comenu
-------
``comenu`` is a simple tool for execute any command in terminal.

Quick Setup
-----------

**macOS**

.. code-block:: bash

   brew install https://raw.githubusercontent.com/dmirubtsov/comenu/master/comenu.rb
   comenu

**Linux**

.. code-block:: bash

   pip3 install comenu
   comenu

**Development**

.. code-block:: bash

   git clone https://github.com/mmeyer724/comenu.git
   cd comenu
   pip3 install -r requirements.txt
   python3 -m comenu

Configuration
-------------
On first run an example configuration file will be created for you, along with the path. For reference, I've added this information here as well.

**OS X**

.. code-block:: bash

   nano ~/Library/Application\ Support/comenu/config.json

**Linux**

.. code-block:: bash

   nano ~/.config/comenu/config.json

**Default contents**

.. code-block:: json

    {
      'targets': [
              {
                  'command': 'ssh root@desktop',
                  'name': 'Desktop',
                  'friendly': 'Connect to desktop by ssh'
              }
          ]
    }

Todo
----
* Submenus
