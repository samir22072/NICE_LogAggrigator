import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import base64

def plot(agentStory,x_param,y_param):
    # Generate data
    x = agentStory[x_param]
    y = agentStory[y_param].value_counts()
    print(y)
    # Create plot
    fig1, ax = plt.subplots()
    labels = y.keys()
    ax.pie(y, labels=labels, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)

    ax.set_title('Visualisation')

    # Save plot as PNG image
    plot_file = 'plot1.png'
    path = 'static/images'
    file1 = f'{path}/{plot_file}'
    fig1.savefig(file1)

    # Convert plot to base64-encoded string
    with open(file1, 'rb') as f:
        plot_data1 = f.read()
    plot_data1 = base64.b64encode(plot_data1).decode('utf-8')

    # Create plot
    fig2, ax = plt.subplots()
    labels = y.keys()
    ax.bar(y.index, y.values)
    ax.set_title('Visualisation')

    # Save plot as PNG image
    plot_file = 'plot2.png'
    path = 'static/images'
    file2 = f'{path}/{plot_file}'
    fig2.savefig(file2)

    # Convert plot to base64-encoded string
    with open(file2, 'rb') as f:
        plot_data2 = f.read()
    plot_data2 = base64.b64encode(plot_data2).decode('utf-8')

    return {'chart1':plot_data1,'chart2':plot_data2}




# base64_image1 = response.json()['chart']['chart1']
#
# decoded_image1 = base64.b64decode(base64_image1)
# image_bytes = BytesIO(decoded_image1)
# image1 = Image.open(image_bytes)
# image1.show()
#
# base64_image2 = response.json()['chart']['chart2']
#
# decoded_image2 = base64.b64decode(base64_image2)
# image_bytes = BytesIO(decoded_image2)
# image2 = Image.open(image_bytes)
# image2.show()