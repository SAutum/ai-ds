library(vars)
library(forecast)
setwd("C:\\Users\\DICE\\Dropbox\\PC (2)\\Desktop\\Time Series\\Tutorial_WS23-24\\Tutorial 6")

#load the dataset and transform into mts object
prod_ind <- read.csv("prod_ind.csv")
prod_ind <- ts(prod_ind[,c(2,3)], start = c(1970, 1), frequency = 4)

#plot both time series
zoo::autoplot.zoo(prod_ind)
zoo::autoplot.zoo(prod_ind,facets = NULL)

#
tsdisplay(prod_ind[,"deu"])
tsdisplay(prod_ind[,"aut"])
#Acf(prod_ind)

#select VAR order
VARselect(prod_ind)

#estimate with lag order = 1
var1 <- VAR(prod_ind, p = 1)

summary(var1)

#Test for residual correlation
sc_test <- serial.test(var1, type = "PT.asymptotic", lags.pt = 8)
print(sc_test)

#Obtain and plot the residuals (ACF and cross-correlation functions (ccf))
par(mfrow=c(2,1))
deu_residuals <- var1$varresult$deu$residuals
aut_residuals <- var1$varresult$aut$residuals
ts.plot(deu_residuals)
ts.plot(aut_residuals)

par(mfrow=c(1,1))
forecast::Acf(cbind(deu_residuals,aut_residuals))

#Granger causality
causality(var1,cause = "deu")$Granger
causality(var1,cause = "aut")$Granger

#Plot the IRFs
plot(irf(var1,ortho = T,impulse = "deu"))
plot(irf(var1,ortho = T,impulse = "aut"))
