import matplotlib.pyplot as plt

plt.plot([250, 500, 1000, 1500, 2000, 2500, 3000, 3500], [61.87, 78.37, 82.92, 88.6, 90.9, 95.27, 97.9, 98.8])
plt.xlabel('No of neurons (per bit)', fontsize = 14)
plt.ylabel('Accuracy (in %)', fontsize = 14)
plt.title('No of neurons vs accuracy for 23 bit addition', fontsize = 20)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)
plt.show()
