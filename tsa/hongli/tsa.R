library(vars)
library(urca)
library(dplyr)
library(zoo)
library(ggplot2)

######### Preliminaries ##########

#### (a)
metals <- read.csv("tsa/hongli/metals.csv")
data$time <- as.yearqtr(data$time, format = "%Yq%q")


#### (b)
data_log <- log(data[,-6])
data_log <- ts(data_log,start=c(1995,1),frequency = 4)

#### (c)
zoo::autoplot.zoo(data_log,facets = NULL)

######### Stationarity ##########

#### (a)
VARselect(data_log[,'rmp'])
aTSA::adf.test(data_log[,'rmp'])#can NOT reject H_0 of non-stationarity. The series is non-stationary at 5% significance level.
aTSA::pp.test(data_log[,'rmp'])#can NOT reject H_0 of non-stationarity.
tseries::kpss.test(data_log[,'rmp'],null = "T") #reject H_0 of trend-stationarity
#both tests point toward non-stat/unit root

VARselect(data_log[,'ipac'])
aTSA::adf.test(data_log[,'ipac']) #reject H_0 of non-stationarity under type 2 with lag = 1.
aTSA::pp.test(data_log[,'ipac'])#can NOT reject H_0 of non-stationarity.
tseries::kpss.test(data_log[,'ipac'],null = "T") #reject H_0 of trend-stationarity
#both tests point toward non-stat/unit root

VARselect(data_log[,'ipcn'])
aTSA::adf.test(data_log[,'ipcn']) #can NOT reject H_0 of non-stationarity
aTSA::pp.test(data_log[,'ipcn'])#can NOT reject H_0 of non-stationarity
tseries::kpss.test(data_log[,'ipcn'],null = "T") #reject H_0 of trend-stationarity
#both tests point toward non-stat/unit root

VARselect(data_log[,'oil'])
aTSA::adf.test(data_log[,'oil']) #reject H_0 of non-stationarity under type 3 with lag = 1 or lag = 3. P.values are 0.0184, 0.0498<0.05
aTSA::pp.test(data_log[,'oil'])#can NOT reject H_0 of non-stationarity
tseries::kpss.test(data_log[,'oil'],null = "T") #can NOT reject H_0 of trend-stationarity
#both tests point toward trend-stationary

#### (b) ADF test and pp test for stationary, kpss test for trend-stationary.
#### ADF and pp tests include lagged terms of the difference of the series in the test equation to account for autocorrelation, which can handle different types of time series data.
#### KPSS complements ADF and pp tests for the presence of trend-stationarity.

#### (c)
diff(data_log[,c('rmp','ipac','ipcn','oil')])

##### (d)
## The significant level is 5%.
VARselect(diff(data_log[,'rmp']))
aTSA::adf.test(diff(data_log[,'rmp']))##reject H_0 of non-stationarity. After the first difference, log(rmp) is stationary. The order of log_rmp is 1.

VARselect(diff(data_log[,'ipac']))
aTSA::adf.test(diff(data_log[,'ipac']))##reject H_0 of non-stationarity. The order of log_ipac is 1.

VARselect(diff(data_log[,'ipcn']))
aTSA::adf.test(diff(data_log[,'ipcn']))##reject H_0 of non-stationarity under Type 2 with lag = 0. The order of log_ipcn is 1.

##The order of log_oil is 0 due to the result in (a).

####### Cointegration & ECM #####

#### (a)
lm_model <- lm(rmp ~ ipac + ipcn + data$time, data=data_log)
summary(lm_model)
VARselect(lm_model$residuals, lag.max = 5, type="const")
aTSA::adf.test(lm_model$residuals)
# with N = 2, T=72 for 5%: -3.33613 - 6.1101/72 - 6.823/(72^2) = -3.42
# -3.42 > -4.03 -> reject H0 of unit root: cointegration
# The order of integration of the resulting residuals is 0. These variables are cointegrated.

test<-ur.df(lm_model$residuals, type = c("drift"), lags = 2)
summary(test)

#### (b)
## Critical value at 5% level is -3.42 for No trend case in ADF test. I obtained it from the paper by MacKinnon (2010, Tbl. 1).
## with N = 2, T=72 for 5%: -3.33613 - 6.1101/72 - 6.823/(72^2) = -3.42

#### (c)
resid<- ts(lm_model$residuals, start = 1995, frequency = 4)
ts.plot(resid)
residual_lagged<- head(stats::lag(resid, -1), -1)

#### (d)
lagged_residual <- as.numeric(residual_lagged)

VARselect(diff(data_log[,c('rmp','ipac','ipcn')]))
VARselect(diff(data_log[,c('rmp','ipac','ipcn')]), exogen = cbind(lagged_residual = c(lagged_residual)))

var1 <- VAR(diff(data_log[,c('rmp','ipac','ipcn')]), p = 5,
            exogen = cbind(lagged_residual = c(lagged_residual)),
            type = "const")
summary(var1$varresult$rmp)


#### (e)
##The coefficient of the error correction term (the lagged residuals) represents the speed at which the dependent variable returns to equilibrium after a shock.
##A negative sign on this coefficient indicates that if the dependent variable is above its long-run equilibrium value, it will decrease in the next period.

#### (f)
vecm_trace <- ca.jo(diff(data_log[,c('rmp','ipac','ipcn')]), K=2, type = "trace", ecdet = "const")
summary(vecm_trace)
#r=0 and r<=1 can be rejected because 60.30 > 34.91 and 29.06 > 19.96
#johansen trace test finds that r=2 (cointegration)

vecm_eigen <- ca.jo(diff(data_log[,c('rmp','ipac','ipcn')]), K=2, type = "eigen", ecdet = "const")
summary(vecm_eigen)
#r=0 and r<=1 can be rejected because 31.24 > 19.77 and 22.63 > 15.67
#johansen eigen test finds that r=2 (cointegration)

#### (g)
# The trace test provides a cumulative measure of the eigenvalues, testing for the number of cointegrating vectors in a sequence. In contrast, the maximum eigenvalue test examines the significance of each eigenvalue separately.

######## VAR ######

####(a)

VARselect(diff(data_log[,c('rmp','oil')]))
var2<-VAR(diff(data_log[,c('rmp','oil')]), p=1)

causality(var2, cause = 'oil')$Granger
#can NOT reject H_0 of d_log_oil do not Granger-cause d_log_rmp
