# Task 1
Consider the following regression model:  wagei = β0 + β1 · educi + β2 · abilityi + ui ,

(1)  where wage denotes the annual wage (in dollars) and educ denotes the number of years spend on education, and ability is the general ability. Assume that MLR.1–3 hold for model (1)

> a)
State the formal zero conditional mean assumption under which the OLS estimator $\hat{\beta}$ of model (1) is unbiased.

A: Under the condition of any combination of education and ability, the
expectation of error term $u$ is always 0.

O: $E[u | educ, ability] = 0$ (independence)

covariance is not enough: $cov(u, educ) = 0$

$E[u | educ] = 0$ -> $cov(u, educ) = 0$
but $cov(u, educ) = 0$ !-> $E[u | educ] = 0$

> b) Suppose that ability is not observable and we consider the underspecified model:  wagei = β0 + β1 · educi + εi . (2)  b) State the formal zero conditional mean assumption under which the OLS estimator βˆ of model (2) is unbiased.

A: Under the conditions of education, the expectation of error term
$\epsilon$ is 0

O: $E[u | educ] = 0$
or $E[\beta_2 ability + u| educ] = 0$

> c) Suppose that MLR.4 holds for model (1). Is the assumption in b) likely to be fulfilled? Explain briefly!

A: No.
$$E[y] = E[\beta_0 + \beta_1 edu + \beta_2 ability + u]$$
$$E[y] = \beta_0 + \beta_1 E[edu] + \beta_2 E[ability]$$
and $\epsilon$ is $\beta_2 ability + u$
The conditional expectation $E[\epsilon | edu]$ will only be zero if
$E[ability | edu]$ is 0

O: linear independence:
$Cov(\epsilon, educ)$ should be 0

-> $Cov(\epsilon, educ)$
= $Cov(\beta_2 ability + u, educ) = \beta_2 Cov(ability, educ)$

$\beta_2$ is likely > 0
$Cov()$ is likely >0

-> MLR.4 in model (2) is violated

# Task 2
Consequences of Omitted Variables in a Specific Sample  Consider the following regression models:  bwghti = β0 + β1 · cigsi + ui , (1)  bwghti = β0 + β1 · cigsi + β2 · faminci + εi , (2)  where bwght denotes the birthweight of a baby in ounces, cigs measures, how many cigarettes a mother has smoked per day during pregnancy and faminc is the family income (in 1, 000 dollars). Further assume that MLR.1–4 hold for model (2).

> a) Do you expect an unchanged, higher or lower coefficient of the variable cigs in model (1) compared to the one in model (2)? Explain briefly!

I assume the family income has positive relationship with birth weight,
since richer family would spend more money on nutrition. I would also assume
a negative relationships between family income and cigs smoked per day.
In all, omittying famin will result in a negative bias. So the $\beta_1$
should be even smaller.

> b)

model 1:

bwght_hat = 119.7719 -0.5137721* cigsi

model 2:

bwght_hat = 116.9741 -0.4634075 * cigsi + 0.09276474 * faminci

$$\tilde{\beta_1} = \hat{\beta_1} + E[\tilde{\beta_1}]$$
$$= \hat{\beta_1} + \beta_2 \cdot \frac{c_{x_1 x_2}}{s_{x_1}^2}$$

$\frac{c_{x_1 x_2}}{s_{x_1}^2}$ is the slope in faminci ~ cigsi

-0.4634075 + 0.09276474 * -0.5429 = -0.513769477346
