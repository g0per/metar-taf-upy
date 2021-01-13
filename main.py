#! upython
# coding=utf-8
#

def descarga_csv(tipo):
    import urequests
    url = CABECERA_URL + tipo +'s'+ FINAL_URL + WX_STATION
    req = urequests.get(url)

    print('Descargando {tipo}'.format(tipo = tipo))

    reporte = req.text.splitlines()[-1].split(',')[0]
    print('{tipo}: {reporte}'.format(tipo = tipo, reporte = reporte))
    return reporte

def apantalla(texto):
    import time
    from machine import I2C, Pin
    from esp8266_i2c_lcd import I2cLcd

    tiempo1 = 5

    i2c_addr = 0x27
    i2c = I2C(scl=Pin(22),sda=Pin(21),freq = 400000)
    lcd = I2cLcd(i2c, i2c_addr,4,20)
 
    for i in range(0,len(texto),40):
        textodisplay = texto[i:i+80]
        lcd.clear()
        lcd.move_to(0, 0)
        print('Mostrando: {textodisplay}'.format(textodisplay=textodisplay))
        lcd.putstr(textodisplay)

        if len(texto) <=40:
            tiempo = tiempo1*2
            print('Esperando {tiempo}s antes de continuar'.format(tiempo=tiempo))
        else:
            if len(texto) >40 and len(texto) <=60:
                tiempo = tiempo1*2
            else:
                tiempo = tiempo1*2
            print('Esperando {tiempo}s antes de subir 2 líneas'.format(tiempo=tiempo))
        time.sleep(tiempo)

def compruebaactu(texto,intervalo):
    from boot import reloj
    
    partido = texto.split(' ')
    encontrado = False
    for i in range(len(partido)):
        if WX_STATION in partido[i]:
            horatexto = partido[i+1][2:6]
            encontrado = True
            break
    if not encontrado:
        return True

    hora = reloj()
    ahora = hora[3]+hora[4]

    print('Hora: {ahora} // Reporte: {horatexto}'.format(horatexto=horatexto,ahora=ahora))

    horanum = int(horatexto)
    ahoranum = int(ahora)
    if intervalo>6:     # 6h para los TAF, 1h para los METAR
        if horanum + intervalo < ahoranum:
            trigger = horanum + intervalo
            print('Trigger: {trigger}'.format(trigger=trigger))
            return True
    else:
        if horanum + intervalo*100 < ahoranum:
            trigger = horanum + intervalo*100
            print('Trigger: {trigger}'.format(trigger=trigger))
            return True

    return False

def main():
    try:
        print('RUN: main')

        global CABECERA_URL, FINAL_URL, WX_STATION
        CABECERA_URL = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource='
        FINAL_URL    = '&requestType=retrieve&format=csv&hoursBeforeNow=24&mostRecent=true&stationString='

        with open('ICAO.dat','r') as station:
            WX_STATION = station.read()
        WX_STATION = WX_STATION.replace('\r','').replace('\n','')

        # EJEMPLO METAR: 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=csv&hoursBeforeNow=24&mostRecent=true&stationString=LEMD'
        # EJEMPLO TAF:   'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=csv&hoursBeforeNow=24&mostRecent=true&stationString=LEMD'
        
        from boot import memoria,hora,reloj
        from machine import reset

        memoria()
        textometar = descarga_csv('metar')
        textotaf = descarga_csv('taf')
        hora(reloj())

        contador = 0
        while True:
            contador +=1
            print('Ciclo {contador}'.format(contador=contador))
            apantalla(textometar)
            apantalla(textotaf)
            memoria()
            if compruebaactu(textometar,55):
                print('Actualizando metar')
                textometar = descarga_csv('metar')
            if compruebaactu(textotaf,6):
                print('Actualizando taf')
                textotaf = descarga_csv('taf')
            memoria()

            if contador == 100:
                with open('log.dat','wb') as archivo:
                    ahora = hora(reloj())
                    archivo.write(ahora)
                reset()
    except Exception as e:
        from machine import reset
        from boot import hora,reloj
        with open('log.dat','wb') as archivo:
            texto = hora(reloj()) + 'main.py' + e
            archivo.write(texto)
        reset()

if __name__ == '__main__':
    main()
