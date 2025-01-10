# Config Systemd

## 1. Create a systemd service file

``` bash
sudo vim /etc/systemd/system/pythonScriptIOT.service
```

### pythonScriptIOT.service

#### general_v1

``` ini
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

```ini
[Unit]
Description=Raspberry Pruebas IoT Service
After=network.target

[Service]
User=root
WorkingDirectory=/home/admin/Desktop/raspberry_pruebas/general_latest
ExecStart=/usr/local/bin/gunicorn -b 0.0.0.0:80 main_server:app
Restart=always

[Install]
WantedBy=multi-user.target

#### general_latest

``` ini
[Unit]
Description=Raspberry Pruebas IoT Service
After=multi-user.target

[Service]
User=root
WorkingDirectory=/home/admin/Desktop/raspberry_pruebas/general_latest
ExecStart=/bin/python3 main_server.py

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

## 3.2 Start the service

```bash
sudo systemctl restart pythonScriptIOT.service
```

## 4. Check the service status

``` bash
sudo systemctl status pythonScriptIOT.service
```

## **Nota importante:**
>
> ```bash
> sudo systemctl disable pythonScriptIOT.service
> sudo systemctl stop pythonScriptIOT.service
> ```
>
