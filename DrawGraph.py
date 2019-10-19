from collections import deque
from tkinter import *

result = []
pts = []
idx = -1
ovalParams = []
showMode = False

def showFrame():
    root = Tk()
    root.title("Draw Maximum Depth Graph without Crossing")
    root.geometry("600x500")
    root.resizable(False, False)
    
    # 이벤트 리스너
    def onClick(pos):
        global ovalParams, showMode
        if showMode:
            return
        ovalParams.append([pos.x-2, pos.y-2, pos.x+2, pos.y+2, "black"])
        canvas.create_oval(ovalParams[-1][0], ovalParams[-1][1], ovalParams[-1][2], ovalParams[-1][3], fill=ovalParams[-1][4])
        textPosX.delete(1.0, "end-1c")
        textPosX.insert(INSERT, f"{pos.x}")
        textPosY.delete(1.0, "end-1c")
        textPosY.insert(INSERT, f"{pos.y}")
        print("position: ", pos.x, pos.y)
        print(textPosX.index(END))
        pts.append((pos.x, pos.y))
        

    def onResetTap():
        global pts, result, idx, ovalParams, showMode
        pts, result, idx, ovalParams, showMode = [], [], -1, [], False
        textPosX.delete(1.0, "end-1c")
        textPosY.delete(1.0, "end-1c")
        canvas.delete("all")

    def onConfirmTap():
        global result, idx, showMode
        if idx == -1 and not result:
            result, showMode = bfsGraph(pts), True
            idx+=1
            canvas.create_line(result[idx])
        else:
            pass
        
    def onPreviousTap():
        global idx, ovalParams
        if not result or idx < 1:
            pass
            return
        canvas.delete("all")
        for ovalParam in ovalParams:
            canvas.create_oval(ovalParam[0], ovalParam[1], ovalParam[2], ovalParam[3], fill=ovalParam[4])
        idx-=1
        canvas.create_line(result[idx])
        
    def onNextTap():
        global idx
        if not result:
            btnConfirm.invoke()
            return
        if idx < len(result)-1:
            canvas.delete("all")
            for ovalParam in ovalParams:
                canvas.create_oval(ovalParam[0], ovalParam[1], ovalParam[2], ovalParam[3], fill=ovalParam[4])
            idx+=1
            canvas.create_line(result[idx])
        else:
            pass

    # 왼쪽 레이아웃    
    canvas = Canvas(root, width=500, height=500,
                        bg="white", relief="solid", bd=1)
    canvas.bind("<Button-1>", onClick)
    canvas.pack(side="left")

    # 오른쪽 레이아웃
    frameButtonBox = Frame(root, width=100, height=500, relief="solid", bd=1)
    frameButtonBox.pack(side="right")

    # X
    textX=Text(frameButtonBox, bg="#f0f0f0", width=1, height=1, relief="flat")
    textX.insert(INSERT,"X")
    textX.place(relx=0.1, rely=0.32)
 
    # x좌표
    textPosX = Text(frameButtonBox, width=8, height=1)
    textPosX.place(relx=0.3, rely=0.32)

    # Y
    textY=Text(frameButtonBox, bg="#f0f0f0", width=1, height=1, relief="flat")
    textY.insert(INSERT,"Y")
    textY.place(relx=0.1, rely=0.37)

    # y좌표
    textPosY = Text(frameButtonBox, width=8, height=1)
    textPosY.place(relx=0.3, rely=0.37)

    # Reset 버튼
    btnReset = Button(frameButtonBox, text="Reset", command=onResetTap,
                        overrelief="solid", width=10)
    btnReset.place(relx=0.1, rely=0.43)
    
    # Confirm 버튼
    btnConfirm = Button(frameButtonBox, text="Confirm", command=onConfirmTap,
                        overrelief="solid", width=10)
    btnConfirm.place(relx=0.1, rely=0.50)

    # Previous 버튼
    btnPrevious = Button(frameButtonBox, text="Previous", command=onPreviousTap,
                        overrelief="solid", width=10)
    btnPrevious.place(relx=0.1, rely=0.57)

    # Next 버튼
    btnNext = Button(frameButtonBox, text="Next", command=onNextTap,
                        overrelief="solid", width=10)
    btnNext.place(relx=0.1, rely=0.64)
        
    root.mainloop()

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

# test_module(bfsGraph, [(3, 3), (1, 2), (2, 1), (4, 2), (5, 1)])
showFrame()
