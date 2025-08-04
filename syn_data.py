import numpy as np
import pandas as pd

#parameters
num_samples = 1000
temperature_mean = 20
temperature_std = 5
humidity_mean = 50
humidity_std = 15
cloud_mean = 36
cloud_std = 7
wind_mean = 11
wind_std= 2
percipation_mean = 5
percipation_std = 2

np.random.seed(40)
temperature_data = np.random.normal(temperature_mean, temperature_std, num_samples)
humidity_data = np.random.normal(humidity_mean, humidity_std, num_samples)
cloud_data = np.random.normal(cloud_mean, cloud_std, num_samples)
wind_data = np.random.normal(wind_mean, wind_std, num_samples)
percipation_data = np.random.normal(percipation_mean, percipation_std, num_samples)


data = pd.DataFrame({
    'temperature': temperature_data,
    'humidity': humidity_data,
    'cloud': cloud_data,
    'wind': wind_data,
    'percipation': percipation_data,
})

print(data.head())

data.to_json("synthetic_data.json", orient="records") #, lines = True )