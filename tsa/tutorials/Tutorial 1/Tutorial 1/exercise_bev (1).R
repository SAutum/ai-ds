#set working dictionary
setwd("C:\\Users\\DICE\\Dropbox\\PC (2)\\Desktop\\Time Series\\Tutorial_WS22-23\\Tutorial 1")

#load data from CSV file, rename, and create year-month (ym) index variable
beverages <- read.csv("bev_data.csv")
colnames(beverages) <- c("date","bvalue")
beverages$ym <- seq.int(nrow(beverages))
str(beverages)

#data.frame to time series object
beverages_ts <- ts(beverages$bvalue, start=1994, frequency = 12)
#rm(beverages, dat)

plot.ts(beverages_ts,col="black",type="o")

monthplot(beverages_ts)

x <- diff(beverages_ts, differences=1)
plot.ts(x)

#decompose
bev_decomp <- decompose(beverages_ts)
plot(bev_decomp)

#run ols regression
model1 <- lm(bvalue ~ ym, beverages)
print(summary(model1))

plot(bvalue ~ ym,beverages)
plot(y=beverages$bvalue, x=beverages$ym)
abline(model1)

plot(model1$residuals)

#diagnostics
par(mfrow=c(1,1))
plot(model1)
