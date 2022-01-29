# Cognite Rice Datathon 2022 Challenge

We have created multiple programs in Python and R which allows us to visualize the wind speed and wind direction in a time series plot. 

## Different Files
- driver.py: This is our main python file which creates two important visualizations. First, we are visualizing wind speed and wind direction in a time series plot for each of three windstations. For our second plot, we are creating a polar plot for the average wind direction and wind speeds for each day across the three windstations (if data is available). 

- datathon.rmd: This is our main R file which creates two important visualizations. This allows us to understand the problem from a mutli-visual perspective in multiple programs. This is integral to our project because different interactive dashboards can use different programming languages. First, we are visualizing wind speed and wind direction in a time series plot for each of three windstations. For our second plot, we are creating a polar plot for the average wind direction and wind speeds for each day across the three windstations (if data is available). 

## Predictions
- We plan to use Markov Models and LSTMs for prediction purposes. Both of these prediction techniques are well vetted for time series forecasting and we believe that these techniques help us come up with accurate predictions. 

## Running the files

- driver.py: Run the following command on terminal "python3 driver.py" and you will see the the time series plot with the polar plot. 
- datathon.rmd: Simply press run on RStudio.

## Output Files:

- Python output: Time_Series_Demo.mov, Polar_Plot.png
- R Output: December 20th, 2021 Example Map R.gif
