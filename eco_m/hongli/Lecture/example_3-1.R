data(gpa1, package = 'wooldridge')

GPAres <- lm(colGPA ~ ACT, data = gpa1)

summary(GPAres)