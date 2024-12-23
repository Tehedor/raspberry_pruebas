## 1. Create a systemd service file

<code>
sudo vim /etc/systemd/system/pythonScriptIOT.service
</code>

### pythonScriptIOT.service
<pre>
[Unit]
Description=Raspberry Pruebas IoT Service
After=multi-user.target

[Service]
User=root
WorkingDirectory=/home/admin/Desktop/raspberry_pruebas/general
ExecStart=/bin/python3 script.py

[Install]
WantedBy=multi-user.target
</pre>


## 2. Reload systemd and enable the service
<code>
sudo systemctl daemon-reload
</code>
<code>
sudo systemctl enable pythonScriptIOT.service
</code>

## 3. Start the service
<code>
sudo systemctl start pythonScriptIOT.service
</code>

## 4. Check the service status
<code>
sudo systemctl status pythonScriptIOT.service
</code>