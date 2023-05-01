import os
import numpy
import pandas
import matplotlib.pyplot as plt
import streamlit as st
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import mean_squared_error, r2_score

distancias = [0.16,0.18,0.16]

st.title("Visualizacion de Datos")

st.subheader("Carga del Archivo")

archivo = st.file_uploader("Elegir archivo:", type=['csv','json'])

def calcularVelocidades(aceleraciones, tiempos):
    print("VELOCIDADES")
    print(aceleraciones)
    print(tiempos)
    velocidades = []
    for n in range(len(tiempos)):
        velocidades.append(aceleraciones[n]*tiempos[n])

    return velocidades

def calcularDiferenciasDeTiempo(tiempos):
    diferencias = []
    for n in range(len(tiempos) - 1):
        diferencias.append(tiempos[n+1]-tiempos[n])

    return diferencias

def calcularAceleraciones(distancias, tiempos):
    print(distancias)
    print(tiempos)
    aceleraciones = []
    for n in range(3):
        aceleraciones.append(calcularAceleracion(distancias[n], tiempos[n], tiempos[n+1]))

    return aceleraciones

def calcularAceleracion(distancia, tiempoX, tiempoX_1):
    print("calculo")
    print(distancia)
    print(tiempoX)
    print(tiempoX_1)
    return (2*distancia)/(tiempoX_1-tiempoX)**2

if archivo is not None:
    file_name = os.path.splitext(archivo.name)

    nombre = file_name[0]
    extension = file_name[1]

    if extension == ".csv":
        data = pandas.read_csv(archivo, header=None)
    elif extension == ".xls" or extension == ".xlsx":
        data = pandas.read_excel(archivo)
    elif extension == ".json":
        data = pandas.read_json(archivo)
    else:
        data = pandas.read_csv(archivo)
    
    st.markdown("#### Data del Archivo:")

    data = data * 0.001

    tiempos_1 = []
    for n in range(4):
        tiempos_1.append(data[n][0])

    tiempos_2 = []
    for n in range(4):
        tiempos_2.append(data[n][1])

    tiempos_3 = []
    for n in range(4):
        tiempos_3.append(data[n][2])

    tiempos_4 = []
    for n in range(4):
        tiempos_4.append(data[n][3])

    aceleraciones = []
    aceleraciones.append(calcularAceleraciones(distancias, tiempos_1))
    aceleraciones.append(calcularAceleraciones(distancias, tiempos_2))
    aceleraciones.append(calcularAceleraciones(distancias, tiempos_3))
    aceleraciones.append(calcularAceleraciones(distancias, tiempos_4))
    dataResultados = pandas.DataFrame(aceleraciones)

    tiempos = [tiempos_1, tiempos_2, tiempos_3, tiempos_4]

    st.markdown("#### Tiempos (segundos):")
    st.dataframe(data)

    st.markdown("#### Aceleraciones (m/s^2):")
    st.dataframe(dataResultados)

    print("TIEMPOS")
    print(tiempos_1)
    print(calcularDiferenciasDeTiempo(tiempos_1))

    st.subheader("Graficas: tiempo vs distancia")
    for n in range(4):
        grafica = plt.figure()
        plt.style.use("fivethirtyeight")
        plt.bar(('1 - 0.16','2 - 0.18','3 - 0.16'), calcularDiferenciasDeTiempo(tiempos[n]), width=0.1)
        plt.title("tiempo vs distancia")
        plt.ylabel("tiempo")
        plt.xlabel("distancia")

        st.pyplot(grafica)

    st.subheader("Graficas: aceleracion vs distancia")
    for n in range(4):
        grafica = plt.figure()
        plt.style.use("fivethirtyeight")
        plt.bar(aceleraciones[n], calcularDiferenciasDeTiempo(tiempos[n]), width=0.1)
        plt.title("tiempo vs aceleracion")
        plt.ylabel("tiempo")
        plt.xlabel("aceleracion")

        st.pyplot(grafica)


    st.subheader("Graficas: velocidad vs distancia")
    for n in range(4):
        grafica = plt.figure()
        plt.style.use("fivethirtyeight")
        plt.bar(calcularVelocidades(aceleraciones[n],calcularDiferenciasDeTiempo(tiempos[n])), calcularDiferenciasDeTiempo(tiempos[n]), width=0.1)
        plt.title("tiempo vs aceleracion")
        plt.ylabel("tiempo")
        plt.xlabel("velocidad")

        st.pyplot(grafica)
