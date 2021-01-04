import plotly.graph_objects as go
from igraph import EdgeSeq

'''
  This method is used to draw the annotations and tooltip of the tree values
'''
def make_annotations(pos, texts, M, font_size=10, font_color='rgb(250,250,250)'):
  L=len(pos)
  if len(texts)!=L:
    raise ValueError('The lists pos and text must have the same len')
  annotations = []
  for k in range(L):
    annotations.append(
    dict(
      text=texts[k],
      x=pos[k][0], y=2*M-pos[k][1],
      xref='x1', yref='y1',
      font=dict(color=font_color, size=font_size),
      showarrow=False)
    )
  return annotations

'''
  This Function is in charge of receiving the `Graph` instance of our Trees
  and  Generate an spatial valid representation using the `layout` method 
  specifying the root of our tree

  `rt` comes from: `Reingold-Tilford Layout`
  https://igraph.org/python/doc/tutorial/tutorial.html#layouts-and-plotting
'''
def plot_tree(G, nr_vertices, v_label):
  lay = G.layout('rt', root=0)

  position = {k: lay[k] for k in range(nr_vertices)}
  Y = [lay[k][1] for k in range(nr_vertices)]
  M = max(Y)

  es = EdgeSeq(G) # sequence of edges
  E = [e.tuple for e in G.es] # list of edges

  L = len(position)
  Xn = [position[k][0] for k in range(L)]
  Yn = [2*M-position[k][1] for k in range(L)]
  Xe = []
  Ye = []
  for edge in E:
      Xe+=[position[edge[0]][0],position[edge[1]][0], None]
      Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

  labels = v_label

  fig = go.Figure()
  fig.add_trace(
    go.Scatter(
      x=Xe,
      y=Ye,
      mode='lines',
      line=dict(color='rgb(200,200,200)', width=1),
      hoverinfo='none'
    )
  )
  fig.add_trace(
    go.Scatter(
      x=Xn,
      y=Yn,
      mode='markers',
      name='bla',
      marker=dict(symbol='circle-dot',
      size=20,
      color='#3345c6',
      line=dict(color='rgb(50,50,50)', width=1)
    ),
    text=labels,
    hoverinfo='text',
    opacity=0.8

    )
  )

  axis = dict(
    showline=False,
    zeroline=False,
    showgrid=False,
    showticklabels=False,
  )

  fig.update_layout(
    title= 'Detailed AST',
    annotations=make_annotations(position, v_label, M),
    font_size=12,
    showlegend=False,
    xaxis=axis,
    yaxis=axis,
    margin=dict(l=40, r=40, b=85, t=100),
    hovermode='closest',
    plot_bgcolor='rgb(210,210,210)',
    paper_bgcolor='rgb(210,210,210)'
  )
  fig.show()