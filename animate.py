import plotly.graph_objects as go
import pandas as pd
import numpy as np
import argparse
import requests


def loading_data(file):
	""" Reads and Return csv file.

		Parameter:
			file (str): Name of the file for reading it

		Returns:
			The data of the file.
	"""
	url = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"
	gets_data = requests.get(url, allow_redirects=True)
	open("data.csv", 'wb').write(gets_data.content)
	return pd.read_csv(file)


def animate_fun(province):
	""" Returns the animated graph showing the number of confirmed cases for the province asked for.

		Parameters:
			province (str): Name of the province 
			                example: "Ontario", "British Columbia", "Quebec", "Alberta", "Saskatchewan", 
			                "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", 
			                "Prince Edward Island"

		Returns:
			figure: Shows number of confirmed cases for a province.
	"""
	graph_df = pd.DataFrame()
	df = loading_data("data.csv")

	for p in df["prname"].unique():
	    # print(province)
	    region_df = df.copy()[df["prname"]==p]
	    region_df.set_index("date", inplace=True)
	    region_df[f"{p}"] = region_df["numconf"]
	    
	    if graph_df.empty:
	        graph_df = region_df[[f"{p}"]]
	    else:
	        graph_df = graph_df.join(region_df[f"{p}"])

    
    # Removing Canada and territories columns so that we get only Province

	graph_df = graph_df.drop(columns=["Canada","Northwest Territories","Yukon","Nunavut","Repatriated travellers"]) 
	# print(graph_df)

	transposed_df = graph_df.transpose()
	
	x_axis = list(range(transposed_df.shape[1]))
	y_axis = list(transposed_df.loc[province:])
	
	province_index = {"Ontario":{'index':0,'color':'#ff6644'},
	"British Columbia": {'index':1,'color':'#f00000'},
	"Quebec":{'index':2,'color':'#bb6688'},
	"Alberta":{'index':3,'color':'#335522'},
	"Saskatchewan":{'index':4,'color':'#33DAFF'},
	"Manitoba":{'index':5,'color':'#000'},
	"New Brunswick":{'index':6,'color':'#FC33FF'},
	"Newfoundland and Labrador":{'index':7,'color':'#ff3311'},
	"Nova Scotia":{'index':8,'color':'#0000ff'},
	"Prince Edward Island":{'index':9,'color':'#ffe476'}}
	for key in province_index:
	    if key == province:
	        row = province_index[key]['index']
	        color = province_index[key]['color']

	frames = []
	for frame in range(1,transposed_df.shape[1]):
		y_axis_frame = list(transposed_df.iloc[row,1:frame])
		x_axis_frame = list(transposed_df.columns)
		curr_frame = go.Frame(data = [go.Scatter(x = x_axis_frame, y = y_axis_frame, mode = "lines", line_color=color,line_width = 3.5)])
		frames.append(curr_frame)

	last_num = transposed_df.loc[province][-1]
	figure = go.Figure(
		data = [go.Scatter(x = np.array([[1]]), y = np.array([3.0]), mode = "lines")],
		layout = {"title":f"Confirmed Cases for {province}",
		          "updatemenus":[{"type":"buttons",
		                         "buttons":[{
		                              "label":"play",
		                              "method":"animate",
		                              "args":[None]}]}],
		           "xaxis":{"title":"Date","range":[0,transposed_df.shape[1]]},
		           "yaxis":{"title":"Total Confirmed Cases","range":[0,last_num+10]}

		          },
		frames = frames
		)
	figure.update_layout(
	    title={
	        'y':0.95,
	        'x':0.5,
	        'xanchor': 'center',
	        'yanchor': 'top'})
	figure.show()


def Main():
	parser = argparse.ArgumentParser()
	parser.add_argument("data1")

	args = parser.parse_args()
	pr = animate_fun(args.data1)
	
if __name__ == '__main__':
	Main()


