# Haproxy Raspberry

1. Instalar haproxy

    ```bash
    sudo apt install haproxy -y
    ```

2. Copiar file configurado

    ```bash
    sudo cp haproxy.cfg  /etc/haproxy/haproxy.cfg
    ```

3. Verifica que el archivo de configuración no contenga errores

    ```bash
    haproxy -c -f /etc/haproxy/haproxy.cfg
    ```

4. Habilitar y reiniciar HAProxy

    ```bash
    sudo systemctl enable haproxy
    sudo systemctl restart haproxy
    ```
