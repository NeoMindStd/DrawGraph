from collections import deque
from tkinter import *

pts = []

def onClick(event):
    print("클릭위치", event.x, event.y)
    pts.append((event.x, event.y))
    print(pts)

def showFrame():
    root = Tk()
    frame = Frame(root, width=800, height=800)
 
     # 왼쪽 마우스 버튼 바인딩
    frame.bind("<Button-1>", onClick) 
 
    frame.pack()
    root.mainloop()

# 1) 클릭 위치를 받는다
# 2) 각 위치에 점을 찍는다
# 3) BFS로 선이 겹치지 않고 연결되는 모든 경우를 구한다.
# 4) 모든 경우를 담은 리스트를 순차적으로 가시화하여 보여준다.
def bfsGraph(points):
    n = len(points)
    result = []
    queue = deque([])
    enQ = queue.append
    deQ = queue.popleft
    for point in points:
        queue.append([point])
        while queue:
            graph = deQ()
            if len(graph) < n:
                for point in points:
                    if point not in graph:
                        enQ(graph+[point])
            else:
                new = list(reversed(graph))
                flag = True
                for i in range(len(result)):
                    cnt = 0
                    for j in range(n):
                        if result[i][j] != new[j]:
                            break
                        cnt += 1
                    if cnt == n:
                        flag = False
                        break
                if flag:
                    result.append(graph)
            
    return result

def test_module(function, params):
    if function == bfsGraph:
        result = bfsGraph(params)
        n = len(result)
        idx = [i for i in range(len(result))]
        for i in range(len(result)):
            result[i] = [idx[i], *result[i]]
        print("\n".join(map(str, result)))

test_module(bfsGraph, [(3, 3), (1, 2), (2, 1), (4, 2), (5, 1)])
showFrame()
