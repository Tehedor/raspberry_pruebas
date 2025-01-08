# Config Systemd

## 1. Create a systemd service file

``` bash
sudo vim /etc/systemd/system/pythonScriptIOT.service
```

### pythonScriptIOT.service

``` XML
[Unit]
Description=Raspberry Pruebas IoT Service
After=multi-user.target

[Service]
User=root
WorkingDirectory=/home/admin/Desktop/raspberry_pruebas/general
ExecStart=/bin/python3 script.py

[Install]
WantedBy=multi-user.target
```

## 2. Reload systemd and enable the service

``` bash
sudo systemctl daemon-reload
```

``` bash
sudo systemctl enable pythonScriptIOT.service
```

## 3. Start the service

```bash
sudo systemctl start pythonScriptIOT.service
```

## 4. Check the service status

``` bash
sudo systemctl status pythonScriptIOT.service
```
