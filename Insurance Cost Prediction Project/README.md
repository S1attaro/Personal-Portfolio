# Summary

This project builds a model to predict medical insurance charges based on age, sex, BMI, number of children, smoking status, and region. The data was cleaned by converting categorical variables like sex and smoker into binary values and creating columns for regions.

The main goal was to see how these factors, especially the relationship between BMI and insurance charges, change depending on smoking status. Using a Lasso regression model, smoking and BMI together had the biggest impact on charges, with smokers paying more as their BMI increases. Other factors like age and number of children also mattered but less so.

The model achieved an R² of 0.877, showing good accuracy while keeping only the most important variables. This makes it useful for health insurance predictions. Future work could explore more advanced models or interactions between variables to improve results.
