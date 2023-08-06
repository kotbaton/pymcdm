import numpy as np
import matplotlib.pyplot as plt
import pymcdm as pm

# Define criteria bounds for the decision problem
bounds = np.array([[0, 1]] * 2, dtype=float)
# Define the Expected Solution Point (or Points) for this problem
esps = np.array([[0.4, 0.4]])
# Create the expert function using ESPExpert class
expert = pm.methods.comet_tools.ESPExpert(esps,
                                          bounds,
                                          cvalues_psi=0.2)
# Generate ESP-guided cvalues based on provided ESP and psi
cvalues = expert.make_cvalues()
# Create and identify COMET model
comet = pm.methods.COMET(cvalues, expert)
# Create a visualization of the characteriscic values,
# ESP and preference function
fig, ax = plt.subplots(figsize=(4, 3.5), dpi=200)
ax, cax = pm.visuals.comet_esp_plot(comet, esps, bounds)
plt.tight_layout()
plt.show()
