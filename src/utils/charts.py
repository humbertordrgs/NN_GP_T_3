import plotly.graph_objects as go

'''
    Small utilities to generate charts for the changes of the fitness during the training
'''
def create_figure():
  return go.Figure()
  
def plot_figure(fig, data, color, title):  
    
  y_axis = [float(x) for x in data]
  fig.add_scatter(
    y=y_axis,
    x=[x+1 for x in range(len(y_axis))],
    mode="lines+markers", 
    textposition="bottom center",
    name=title,
    line={"color": color, "width": 1}
  )
  fig.update_layout(
    title="Fitness chart",
    xaxis_title="Generations",
    yaxis={"title": "Accuracy in Test", "tickformat": ".5f"},
    font=dict(
      family="Courier New, monospace",
      size=14,
      color="#7f7f7f"
    )
  )