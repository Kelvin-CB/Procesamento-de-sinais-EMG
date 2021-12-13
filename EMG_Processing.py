# %%
'''
    File name: Procesammento de sinais EMG.py
    Author: Kelvin Carvalho
    Date created: 19/11/2019
    Date last modified: 16/12/2019
    Python Version: 3.7
'''


#bibliotecas importadas
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
matplotlib.pyplot.show()
matplotlib.interactive(True)
import scipy as sp
from scipy import signal
from sklearn.cluster import KMeans
from tkinter import *
from tkinter import filedialog 
from tkinter.filedialog import askopenfilename
from tkinter import ttk
master = Tk()
master.title('Processamento de EMG')




def callback():
    path = askopenfilename(title='Choose a file') #Variavel qu contém o endereço do dataset 
    e.delete(0, END)  # Limpa texto atual na entrada
    e.insert(0, path)  # Insere o path do arquivo escolhido na entrada
    highn = bh.get() #Frequencia para o bandpass
    lown = bl.get() #Frequencia para o banpass
    fqn = fqq.get() #Amostra de frequência base
    
    
    if path:
        if (len(highn)!=0 and len(lown)!=0 and len(fqn)!=0):
            high = float(highn)#Definindo frequencia do bandpass como do tipo float
            low = float(lown)#Definindo frequencia do bandpass como do tipo float
            fq = int(fqn)#definindo frequencia base como do tipo Inteiro
            dataset = np.genfromtxt(path,skip_header=1) #Abertura do dataset que contém os dados EMG
            time = dataset[:,0] #Definindo Tempo(eixo X) como coluna 0 do dataset
            emg = dataset[:,1] #Definindo EMG(eixo Y) como culuna 1 do dataset
            correctedmean = emg - np.mean(emg) #Correção do valor médio do dataset
            b, a = sp.signal.butter(4, [high,low], btype='bandpass') #Primeira fltragem por Bandpass
            filtering = sp.signal.filtfilt(b, a, correctedmean) #Processamento do sinal EMG
            rectified = abs(filtering) #Retificação do sinal

            def movingaverage(values, window): #Função geral do Filtro de Média movel
                weight = np.repeat(1.0,window)/window
                smas = np.convolve(values, weight, 'valid')
                return smas
            MAV1 = movingaverage(rectified, 2*fq) #Chamado da função nos dados de EMG Retificado
            TIME1 = movingaverage(time, 2*fq) #Chamado da função nos dados do tempo

            X = np.column_stack((TIME1, MAV1)) #K-mean Clustering
            kmeans = KMeans(n_clusters= int(fq/2)) #Numero de Clusters
            kmeans.fit(X)

            def rawdata(time, emg): #Função de plotagem do Gráfico de Dados em Raw Mode
                plt.plot(time, emg)
                plt.xlabel('Tempo')
                plt.ylabel('EMG')
                plt.title('Gráfico do "Raw data"')
                plt.savefig('rawdata.png', bbox_inches='tight')

            def correctmean(time, correctedmean): #Função de plotagem do Gráfico de Correção do Valor Médio
                plt.plot(time, correctedmean)
                plt.locator_params(axis='x', nbins=4)
                plt.locator_params(axis='y', nbins=4)
                plt.xlabel('Tempo')
                plt.ylabel('EMG (uV)')
                plt.title('Valor médio ajustado')
                plt.savefig('correctmean.png', bbox_inches='tight')

            def filteremg(time, filtering): #Função de plotagem do Gráfico de Filtro Bandpass
                plt.plot(time, filtering)
                plt.locator_params(axis='x', nbins=4)
                plt.locator_params(axis='y', nbins=4)
                plt.xlabel('Tempo')
                plt.ylabel('EMG (uV)')
                plt.title('Filtragem EMG')
                plt.savefig('filteremg.png', bbox_inches='tight')

            def rectification(time, rectified): #Função de plotagem do Gráfico de Retificação de Sinal
                plt.plot(time, rectified)
                plt.locator_params(axis='x', nbins=4)
                plt.locator_params(axis='y', nbins=4)
                plt.xlabel('Tempo')
                plt.ylabel('EMG (uV)')
                plt.title('Sinal Retificado')
                plt.savefig('rectification.png', bbox_inches='tight')

            def mavfilter(TIME1, MAV1): #Função de plotagem do Gráfico de Filtro de Média Movel
                plt.plot(TIME1, MAV1)
                plt.locator_params(axis='x', nbins=4)
                plt.locator_params(axis='y', nbins=4)
                plt.xlabel('Tempo')
                plt.ylabel('EMG (uV)')
                plt.title('Filtro de Média Movel')
                plt.savefig('mavfilter.png', bbox_inches='tight')

            def kclustering(time, rectified, TIME1, MAV1, X):#Função de plotagem do Gráfico de K-Means Clustering
                plt.plot(time, rectified, color= 'r',  alpha=0.5, label="Sinal Retificado")
                plt.plot(TIME1,MAV1, color= 'g',label="Filtro de Média Movel")
                plt.scatter(X[:,0], X[:,1], c=kmeans.labels_, cmap='Blues', label="K Means")
                plt.scatter(kmeans.cluster_centers_[:,0] ,kmeans.cluster_centers_[:,1], color='black', label="Centros de Interesse")
                plt.legend(loc="upper left")
                plt.xlabel('Tempo')
                plt.ylabel('EMG (uV)')
                plt.savefig('kclustering.png', bbox_inches='tight')

            def savetext(time, rectified, TIME1, MAV1, X, correctedmean): #função geral de exportação de dataset
                option = savefile.get()

                if option in ["Corrected Mean"]: #Função para exportar o dataset até a fase de Correção de Valor Médio
                    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
                    if f!=None:
                        for i,j in zip(time,correctedmean):
                            f.write(str(i)+" "+str(j)+"\n")
                        f.close()

                if option in ["Bandpass"]: #Função para exportar o dataset até a fase de FIltros Bandpass
                    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
                    if f!=None:
                        for i,j in zip(time, filtering):
                            f.write(str(i)+" "+str(j)+"\n")
                        f.close()

                if option in ["Rectification"]: #Função para exportar o dataset até a fase de Retificação de Sinal
                    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
                    if f!=None:
                        for i,j in zip(time, rectified):
                            f.write(str(i)+" "+str(j)+"\n")
                        f.close()

                if option in ["MAV1"]: #Função para exportar o dataset até a fase de Filtro de Média Movel
                    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
                    if f!=None:
                        for i,j in zip(TIME1, MAV1):
                            f.write(str(i)+" "+str(j)+"\n")
                        f.close()

                if option in ["K-Means"]: #Função para exportar o dataset até a fase de K-Means clustering
                    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
                    if f!=None:
                        for i,j in zip(X[:,0],X[:,1]):
                            f.write(str(i)+" "+str(j)+"\n")
                        f.close()



            #Criação e organização dos widgets de seleção de gráfico e dataset no ambiente gráfico
            grafico1 = Button(right_frame, text="RawData", command=lambda:rawdata(time, emg))
            grafico1.grid(row=0, sticky="ew")    
            grafico2 = Button(right_frame, text="Corrected Mean", command=lambda:correctmean(time, correctedmean))
            grafico2.grid(row=1, sticky="ew")    
            grafico3 = Button(right_frame, text="Bandpass", command=lambda:filteremg(time, filtering))
            grafico3.grid(row=2, sticky="ew")    
            grafico4 = Button(right_frame, text="Retification", command=lambda:rectification(time, rectified))
            grafico4.grid(row=3, sticky="ew")    
            grafico5 = Button(right_frame, text="MAV", command=lambda:mavfilter(TIME1, MAV1))
            grafico5.grid(row=4, sticky="ew")    
            grafico6 = Button(right_frame, text="K-Means", command=lambda:kclustering(time, rectified, TIME1, MAV1, X))
            grafico6.grid(row=5, sticky="ew")  
            savefile = ttk.Combobox(option_frame, 
                                    values=[
                                            "Corrected Mean", 
                                            "Bandpass",
                                            "Rectification",
                                            "MAV1",
                                            "K-Means"])
            savefile.grid(row=0)
            saveb = Button(option_frame, text="Save", command=lambda:savetext(time, rectified, TIME1, MAV1, X, correctedmean))
            saveb.grid(row=0,column=1)
        else: print("Defina os parâmetros de forma correta")



#Criação das frames do ambiente gráfico
top_frame = Frame(master)
file_frame = Frame(master)
right_frame = Frame(master)
option_frame = Frame(master)

#Organização das frames na matriz
top_frame.grid(row=0)
file_frame.grid(row=3)
option_frame.grid(row=3, column=1)
right_frame.grid(row=0, column=1)
    


#Criação dos widgets de ajuste de frequências e seleção de arquivo do ambiente gráfico
w = Label(file_frame, text="Local do arquivo:")
e = Entry(file_frame, text="")
b = Button(file_frame, text="Procurar", command=callback)
bh = Entry(top_frame, text="")
bhlabel = Label(top_frame, text="Frequência Highpass:")
bl = Entry(top_frame, text="")
bllabel = Label(top_frame, text="Frequência Lowpass:")
fqq = Entry(top_frame, text="")
fqqlabel = Label(top_frame, text="Frequência Base:")

#Organização dos widgets de ajuste de frequências e seleção de arquivo na matriz
w.grid(row=0)
e.grid(row=0, column=1)
b.grid(row=0, column=2)
bhlabel.grid(row=0)
bh.grid(row=0, column=1)
bllabel.grid(row=1)
bl.grid(row=1, column=1)
fqqlabel.grid(row=2)
fqq.grid(row=2,column=1)

master.mainloop()



# %%


# %%



