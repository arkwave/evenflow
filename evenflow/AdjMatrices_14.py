import numpy as np

#Computes an Adjacency Matrix A
#Computes the Characteristic Lag Which is the First Significant Lag
#Takes the Transfer Information Matrix and the Significance Thresholds

def AdjMatrices(T, SigThreshT,TvsIzero):
    def helper1(sX, sY, lag):
        Abinary[lag, sX,sY] = 1
        AwtdCut[lag, sX,sY] = T[lag, sX,sY]
        LastSigLag[sX,sY] = lag+1
        nSigLags[sX, sY] = nSigLags[sX, sY] + 1
        return

    def helper2(sX, sY, lag):
        charLagMaxPeak[sX, sY] = lag+1
        TcharLagMaxPeak[sX, sY] = T[lag, sX,sY]
        return

    def helper3(sX, sY, lag):
        charLagFirstPeak[sX, sY] = lag+1
        TcharLagFirstPeak[sX, sY] = T[lag, sX,sY]
        return


    nLags, nSignals, junk = np.shape(T)

    Abinary = np.zeros((nLags, nSignals,nSignals))
    Awtd = np.empty((nLags, nSignals, nSignals ))
    Awtd.fill(np.NAN)

    AwtdCut = np.zeros((nLags, nSignals, nSignals ))
    charLagFirstPeak = np.zeros((nSignals, nSignals))
    TcharLagFirstPeak = np.zeros((nSignals,nSignals))
    charLagMaxPeak = np.zeros((nSignals,nSignals))
    TcharLagMaxPeak = np.zeros((nSignals, nSignals))
    TvsIzerocharLagMaxPeak = np.zeros((nSignals, nSignals))
    nSigLags = np.zeros((nSignals, nSignals))
    FirstSigLag = np.empty((nSignals, nSignals))
    FirstSigLag.fill(np.NAN)

    LastSigLag = np.empty((nSignals, nSignals))
    LastSigLag.fill(np.NAN)

    for sX in range(nSignals):
        for sY in range(nSignals):
            FirstPeakFlag = 0
            FirstSigFlag = 0 

            Awtd = T

            #check the first Lag
            lag = 0
            if T[lag, sX,sY] > SigThreshT[sX,sY]:
                helper1(sX, sY, lag)
                helper2(sX, sY, lag)
                
                TvsIzerocharLagMaxPeak[sX, sY] = TvsIzero[lag, sX, sY]
                FirstSigFlag  = 1 

                if nLags > 1:
                    if T[lag, sX, sY] > T[lag+1, xS, sY]:
                        helper3(sX, sY, lag)
                        FirstPeakFlag = 1
                else:
                    helper3(sX, sY, lag)
                    FirstPeakFlag = 1

            #nlags: number of lags
            #re-check indexing becaus matlab uses indexing start with 1, python uses 0.
            #create function for 2 lag checkings (note the difference) for possible improvement 
            #check the other lag
            if nLags > 1:
                for lag in range(1, nLags - 1):
                    if T[lag, sX, sY] > SigThreshT[sX, sY]:
                        helper1(sX, sY, lag)
                        if FirstSigFlag == 0:
                                FirstSigLag[sX, sY] = lag+1
                                FirstSigFlag = 1
                        if FirstPeakFlag == 0 and T[lag, sX, sY ] > T[lag - 1, sX, sY ] and T[lag, sX, sY ] > T[ lag + 1, sX, sY]:
                            helper3(sX, sY, lag)
                            FirstPeakFlag =1
                        if T[lag, sX, sY ] > TcharLagMaxPeak[sX, sY]:
                            helper2(sX, sY, lag)
                            TvsIzerocharLagMaxPeak[sX, sY] = TvsIzero[lag, sX, sY ]
                #check the last lag
                lag = nLags - 1 

                if T[lag, sX, sY ] > SigThreshT[sX, sY]:
                            helper1(sX, sY, lag)
                            if FirstSigFlag == 0:
                                FirstSigLag[sX, sY] = lag+1
                                FirstSigFlag = 1
                            if FirstPeakFlag == 0 and T[lag, sX, sY ] > T[lag - 1, sX, sY ]:
                                charLagFirst[sX,sY]=lag;
                                TcharLagFirst[sX,sY]=T[lag,sX,sY];
                                FirstPeakFlag =1
                            if T[lag, sX, sY] > TcharLagMaxPeak[sX, sY]:
                                helper2(sX, sY, lag)
                                TvsIzerocharLagMaxPeak[sX, sY] = TvsIzero[lag, sX, sY]

    return (Abinary, Awtd, AwtdCut, charLagFirstPeak, TcharLagFirstPeak, charLagMaxPeak, TcharLagMaxPeak, TvsIzerocharLagMaxPeak, nSigLags, FirstSigLag, LastSigLag)





