# set directory to the location of the data
setwd("/home/hongli/MyApps/aids/tsa/tutorials/Tutorial 1/Tutorial 1")

# load the bev_data.csv file
beverages <- read.csv("bev_data.csv")
# reanme the columns
colnames(beverages) <- c("date","bvalue")
# create a year-month index variable
beverages$ym <- seq.int(nrow(beverages))

# transform the series into a time series object
beverages_ts <- ts(beverages$bvalue, start=1994, frequency = 12)

# plot the time series
plot.ts(beverages_ts,col="black",type="o")

# monthplot
monthplot(beverages_ts)

# create the first difference of the series and plot it
x <- diff(beverages_ts, differences=1)
plot.ts(x)

# decompose the series
bev_decomp <- decompose(beverages_ts)
plot(bev_decomp)

# linear trend model via olS
model1 <- lm(bvalue ~ ym, beverages)
print(summary(model1))

# diagnostic plots
par(mfrow=c(1,1))
plot(model1)
