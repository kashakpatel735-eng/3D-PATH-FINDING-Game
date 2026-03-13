import streamlit as st
import numpy as np
import heapq
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Sky blue UI
st.markdown("""
<style>

.stApp{
background-color:#87CEEB;
}

h1{
text-align:center;
color:black;
}

</style>
""", unsafe_allow_html=True)

st.title("🎮 3D Path Finding Game")

GRID = 7

maze = np.array([
[0,0,1,0,0,0,0],
[0,0,1,0,1,1,0],
[0,0,0,0,0,1,0],
[1,1,1,1,0,1,0],
[0,0,0,1,0,0,0],
[0,1,0,0,0,1,0],
[0,1,0,1,0,0,0]
])

# Player inputs
st.sidebar.header("Player Coordinates")

p1x = st.sidebar.number_input("Player 1 X",0,GRID-1,0)
p1y = st.sidebar.number_input("Player 1 Y",0,GRID-1,0)

p2x = st.sidebar.number_input("Player 2 X",0,GRID-1,6)
p2y = st.sidebar.number_input("Player 2 Y",0,GRID-1,6)

start=(p1x,p1y)
goal=(p2x,p2y)

# A* Algorithm
def astar(maze,start,end):

 open_list=[]
 heapq.heappush(open_list,(0,start))

 came_from={}
 g={start:0}

 while open_list:

  _,current=heapq.heappop(open_list)

  if current==end:

   path=[]
   while current in came_from:
    path.append(current)
    current=came_from[current]

   path.append(start)
   return path[::-1]

  x,y=current

  for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:

   nx,ny=x+dx,y+dy

   if 0<=nx<GRID and 0<=ny<GRID and maze[nx][ny]==0:

    new_cost=g[current]+1

    if (nx,ny) not in g or new_cost<g[(nx,ny)]:

     g[(nx,ny)]=new_cost

     h=abs(nx-end[0])+abs(ny-end[1])

     f=new_cost+h

     heapq.heappush(open_list,(f,(nx,ny)))

     came_from[(nx,ny)]=current

 return []


fig=go.Figure()

# Maze
for i in range(GRID):
 for j in range(GRID):

  if maze[i][j]==1:
   color="red"
   z=2
  else:
   color="lightgreen"
   z=0.3

  fig.add_trace(go.Scatter3d(
  x=[i],
  y=[j],
  z=[z],
  mode="markers",
  marker=dict(size=22,color=color)
  ))

# Player1
fig.add_trace(go.Scatter3d(
x=[start[0]],
y=[start[1]],
z=[3],
mode="markers",
marker=dict(size=14,color="blue"),
name="Player 1"
))

# Player2
fig.add_trace(go.Scatter3d(
x=[goal[0]],
y=[goal[1]],
z=[3],
mode="markers",
marker=dict(size=14,color="gold"),
name="Player 2"
))

# Find path
if st.button("Find Path"):

 path=astar(maze,start,goal)

 if path:

  px,py=zip(*path)

  fig.add_trace(go.Scatter3d(
  x=px,
  y=py,
  z=[3]*len(px),
  mode="lines+markers",
  line=dict(width=10,color="cyan"),
  marker=dict(size=6,color="cyan"),
  name="Shortest Path"
  ))

fig.update_layout(
height=700,
template="plotly_white",
scene=dict(
zaxis=dict(visible=False),
camera=dict(eye=dict(x=1.7,y=1.7,z=1.2))
)
)

st.plotly_chart(fig,use_container_width=True)
