import numpy as np
import matplotlib.pyplot as plt

x_data = np.arange(1, 32, 1)
y_val = np.random.randint(30, 300, 31)
#print x_data
#print y_val
fig = plt.figure()  
plt.bar(x_data, y_val, 1, color="green")  
plt.xlabel("data")  
plt.ylabel("value")  
plt.title("pm2.5 chart")  

plt.savefig("pm2p5chart.jpg")
