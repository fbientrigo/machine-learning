"""
Contiene las funciones utiles en el desarrollo del trabajo,
funciones que podrian ser de ayuda en otras ocaciones

"""


def split_in_3(dataframe, splits = [0.60, 0.25, 0.15], shuffle=True, random_state = 32):
    """
    Utilizando sklearn.model_selection.train_test_split()
    divide los datos en 3, de manera que pueden ser divididos en:
    - training data
    - cross validation data (probar el modelo entre epochs)
    - final testing (una vez este feliz con un modelo, un test final para anotar el resultado)

    se debe de tener en cuenta que no se debe seguir entrenando luego de medir 
    con el final testing, pues dejaria de ser una medida correcta para el modelo
    """
    # importado dentro de la función para permitir mayor libertad y modularidad
    import sklearn.model_selection as model_selection 

    if sum(splits) == 1 and len(splits) == 3: # comprueba la condición de la función
        data1, data_m = model_selection.train_test_split(
            dataframe, train_size= splits[0], random_state= random_state, shuffle=shuffle
        )
        # data_m posee un % de (1- splits[0])
        # por tanto el split debe de actualizar el porcentaje para obtener la cantidad correcta
        data2, data3 = model_selection.train_test_split(
            data_m, train_size= splits[1]/(1-splits[0]), random_state= random_state, shuffle=shuffle
        )
        
    else: # permite indicar un error de que no se esta usando bien la función
        raise Exception("Los porcentajes de splits deben de sumar 1.0 y deben de ser 3")

    # es importante el testing, pues permite evitar comportamiento indeseado
    # gracias al testing podemos probar la función correctamente
    assert len(data1) == len(dataframe) * splits[0]
    assert len(data2) == len(dataframe) * splits[1]
    assert len(data3) == len(dataframe) * splits[2]
    print(f"data1:{splits[0]}, data2:{splits[1]}, data3:{splits[2]}")

    assert len(data1)+len(data2)+len(data3) == len(dataframe)
    print("Division funciono correctamente")
    return data1, data2, data3


# guardado todo dentro de una función:
def transform_fourier_plot(data, tstep, total_time, N, title):
    # first weight configutation and 100 percent of blade
    acceleration_data = dataframe[(dataframe['wconfid'] == 1) & (dataframe['pctid'] == 100)].x.values


    # =================datos=======================
    # tstep sample time interval in seconds
    Fs = 1/tstep    # sample frequency (Hz)

    N_ = int(Fs * total_time) # number of samples
    assert N_ == N # para comprobar errores

    fstep = Fs / N # frequency interval

    # ==============================================
    t = np.linspace(0, (N-1) * tstep, N) 
    f = np.linspace(0, (N-1) * fstep, N)


    fft_data = np.fft.fft(data) / N
    # se divide sobre N para normalizar
    fft_mag = np.abs(fft_data)


    # dada mi maxima frecuencia puedo reconstruir hasta bajo la mitad de esta
    f_plot = f[0:int(N/2+1)] #nyquist theorem
    fft_mag_plot = 2 * fft_mag[0:int(N/2+1)] # cuenta por la energia de las frecuencias negativas
    fft_mag_plot[0] = fft_mag_plot[0] / 2 # el primer componente solo aparece una vez, no 2


    fig, ax = plt.subplots(nrows = 2, ncols=1)
    ax[0].plot(t, data, '.-')
    ax[0].set_xlabel('t [s]')
    ax[1].plot(f_plot, fft_mag_plot, '.-')
    ax[1].set_xlabel('f [Hz]')
    fig.suptitle(title)
    plt.show()