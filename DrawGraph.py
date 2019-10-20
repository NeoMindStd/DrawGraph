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
        textCurrentIdx.delete(1.0, "end-1c")
        textEndIdx.delete(1.0, "end-1c")
        canvas.delete("all")

    def onConfirmTap():
        global result, idx, showMode
        try:
            if idx == -1 and not result:
                result, showMode = bfsGraph(pts), True
                print("필터링 전: %d개" %len(result))
                result = list(filter(lambda x: not isCrossGraph(x), result))
                print("필터링 후: %d개" %len(result))
                idx+=1
                canvas.create_line(result[idx])
                textCurrentIdx.insert(INSERT, idx+1)
                textEndIdx.insert(INSERT, len(result))
            else:
                pass
        except:
            print("***점을 2개 이상 찍어주세요***")
            btnReset.invoke()
            
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
        textCurrentIdx.delete(1.0, "end-1c")
        textCurrentIdx.insert(INSERT, idx+1)
        
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
            textCurrentIdx.delete(1.0, "end-1c")
            textCurrentIdx.insert(INSERT, idx+1)
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
    
    # Now
    textNow=Text(frameButtonBox, bg="#f0f0f0", width=4, height=1, relief="flat")
    textNow.insert(INSERT,"Now:")
    textNow.place(relx=0.0, rely=0.87)
    
    # current idx
    textCurrentIdx=Text(frameButtonBox, bg="#f0f0f0", width=6, height=1, relief="flat")
    textCurrentIdx.place(relx=0.4, rely=0.87)

    # End
    textEnd=Text(frameButtonBox, bg="#f0f0f0", width=4, height=1, relief="flat")
    textEnd.insert(INSERT,"End:")
    textEnd.place(relx=0.0, rely=0.92)

    # end idx
    textEndIdx=Text(frameButtonBox, bg="#f0f0f0", width=6, height=1, relief="flat")
    textEndIdx.place(relx=0.4, rely=0.92)
        
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

def ccw(pos1, pos2, pos3):
    x1, x2, x3 = pos1[0], pos2[0], pos3[0]
    y1, y2, y3 = pos1[1], pos2[1], pos3[1]
    tmp = x1*y2+x2*y3+x3*y1 - y1*x2-y2*x3-y3*x1
    if tmp > 0:
        return 1
    elif tmp < 0:
        return -1
    else:
        return 0

def isCross(a, b, c, d):
    abc, abd, cda, cdb = ccw(a, b, c), ccw(a, b, d), ccw(c, d, a), ccw(c, d, b)
    ab, cd = abc*abd, cda*cdb
    if ab == 0 and cd == 0 and (sum([abc**2, abd**2, cda**2, cdb**2])==0  or (a!=c and a!=d and b!=c and b!=d)):
        if a > b:
            a, b = b, a
        if c > d:
            c, d = d, c
        return c<b and a<d
    return ab<0 and cd<0

def isCrossGraph(graph):
    for i in range(len(graph)-1):
        for j in range(len(graph)-1):
            if i != j:
                if isCross(graph[i], graph[i+1], graph[j], graph[j+1]):
                    return True
    return False

def testDriver(function, params):
    if function == bfsGraph:
        result = bfsGraph(params)
        n = len(result)
        idx = [i for i in range(len(result))]
        for i in range(len(result)):
            result[i] = [idx[i], *result[i]]
        print("\n".join(map(str, result)))
    elif function == isCrossGraph:
        print(f"{params}: {isCrossGraph(params)}")

showFrame()
