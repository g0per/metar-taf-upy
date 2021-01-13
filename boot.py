#! upython
# coding=utf-8
#

def wifi_connect():
    ''' Network setup'''
    #print('RUN: boot.wifi_connect')

    import network,time,os,ntptime

    if 'wifi.dat' in os.listdir():      # Lee fichero de contraseñas
        with open('wifi.dat','r') as archivowifiDB:
            guardados_list = archivowifiDB.readlines()

        if len(guardados_list) % 2 == 1:
            print('Comprobar formato de wifi.dat\n\t El formato correcto es:\n\t\tSSID1\n\t\tpass1\n\t\tSSID2\n\t\tpass2\n\t\tetc')
        else:
            guardados = {}
            contador = 1
            numeroguardados = len(guardados_list)/2
            for i in range(numeroguardados):
                guardados_list[i] = guardados_list[i].replace('\r','').replace('\n','')

            for i in guardados_list[::2]:       # Lo convierte a diccionario
                guardados[i] = guardados_list[contador]
                contador +=2
            print('{tamaño} SSIDs guardadas'.format(tamaño = len(guardados)))

            wifi = network.WLAN(network.STA_IF)
            wifi.active(False)
            wifi.active(True)
            if not wifi.isconnected():      # Escanea, y comprueba en orden si están guardados credenciales para conectarse
                disponibles = wifi.scan()
                activas = []
                for i in disponibles:
                    if i[0].decode('ascii') in guardados:
                        activas.append(i)
                if len(activas) == 0:
                    print('ERROR: Redes configuradas no disponibles.')
                else:
                    print('Conectando WiFi')
                    wifi.connect(activas[0][0].decode('ascii'),guardados[activas[0][0].decode('ascii')])
                    while not wifi.isconnected():
                        print('Esperando conexión')
                        time.sleep(1)
                ntptime.settime()

def memoria():
    ''' Free memory'''
    import gc
    gc.collect
    memoria = gc.mem_free()
    print('Memoria disponible: {memoria}'.format(memoria = memoria))

def reloj():
    import time
    currenttime = []
    for i in time.localtime(time.time())[:6]:
        i = str(i)
        currenttime.append(i)
    for i in range(1,6):
        if len(currenttime[i]) == 1:
            currenttime[i] = '0'+currenttime[i]
    return currenttime

def hora(str_reloj):
    print('Hora: {yyyy}{mm}{dd} {hh}{min}:{ss}'.format(yyyy=str_reloj[0],mm=str_reloj[1],dd=str_reloj[2],hh=str_reloj[3],min=str_reloj[4],ss=str_reloj[5]))

def main():
    try:
        print('RUN: boot')
        memoria()
        wifi_connect()
        hora(reloj())
    except Exception as e:
        from machine import reset
        with open('log.dat','wb') as archivo:
            texto = hora(reloj()) + 'boot.py' + e
            archivo.write(texto)
if __name__ == '__main__':
    main()
