import random
import numpy as np
import heapq
import time
import tkinter as tk



class HangDoiUuTien:                    #hang doi uu tien hien thuc bang haepq
    def __init__(self):
        self._data = []
        self._index = 0
        self.count=0
    def push(self, item, priority):
        heapq.heappush(self._data, (priority, self._index, item))
        self._index += 1
        self.count +=1
    def pop(self):
        self.count -=1
        return heapq.heappop(self._data)[-1]

#init_puzzle
def DauVao(test,n):
    return np.array(test).reshape(n,n)

def TimOTrong(trangThai):
    return tuple(np.argwhere((trangThai == 0))[0])

#check cac buoc di chuyen hop le
def KiemTraHanhDongHopLe(DiChuyen,viTriOTrong,trangThai):
    n =len(trangThai[0])
    xPlayer, yPlayer = viTriOTrong
    x1, y1 = xPlayer + DiChuyen[0], yPlayer + DiChuyen[1]
    if (((x1>=0) & (x1<n)) & ((y1>=0) & (y1<n))):
        return 1
    else:
        return 0
    
#tuple chua cac buoc di chuyen
def HanhDongHopLe(viTriOTrong,trangThai):
    cacBuocDiChuyen = [[-1,0,'up'],[1,0,'down'],[0,-1,'left'],[0,1,'right']]
    diChuyenHopLe = []
    for diChuyen in cacBuocDiChuyen:
        
        if KiemTraHanhDongHopLe(diChuyen, viTriOTrong, trangThai):
            diChuyenHopLe.append(diChuyen)
        else: 
            continue
    return tuple(tuple(x) for x in diChuyenHopLe) 

#cac trang thai con duoc sinh ra tu cac buoc di chuyen hop le
def CapNhatTrangThai(ViTriOTrong, trangThai, diChuyen):
    xPlayer, yPlayer = ViTriOTrong
    x1, y1 = xPlayer + diChuyen[0], yPlayer + diChuyen[1]
    ViTriOTrongMoi = [xPlayer + diChuyen[0], yPlayer + diChuyen[1]] 
    ViTriOTrongMoi = tuple(ViTriOTrongMoi)
    n = len(trangThai[0])
    trangThaiMoi = np.zeros((n,n),dtype=int)
    for x in range(n):
        for y in range(n):
            trangThaiMoi[x][y]=trangThai[x][y]
    trangThaiMoi[xPlayer][yPlayer] = trangThai[x1][y1]
    trangThaiMoi[x1][y1] = 0
    return ViTriOTrongMoi, trangThaiMoi

#tao goal_puzzle
def TrangThaiDich(trangThai):
    n=len(trangThai[0])
    TrangThaiDich=[]
    for x in range(1,n*n):           
        TrangThaiDich.append(x)
    TrangThaiDich.append(0)
    return np.array(TrangThaiDich)


def KiemTraTrangThaiDich(trangThai,trangThaiDich):
    n=len(trangThai[0])
    a = trangThai.reshape(1,n*n)[0]
    return (a == trangThaiDich).all()

#check tra ve vi tri dung cua init_puzzle so voi goal_puzzle
def index(m,n):
    if m==0:
        return n-1,n-1
    x=(m-1)//n
    y=(m-1)%n
    return x,y

#heuristic theo ham uoc luong h(1)
def heuristic(trangThai):
    n=len(trangThai[0])
    sum=0
    for x1 in range(n):
        for y1 in range(n):
            x2 ,y2 =index(trangThai[x1][y1],n)
            if (x1==x2) & (y1==y2):
                if trangThai[x1][y1]!=0:
                    sum=sum+1
    return n*n-sum

def Astar(trangThai):
    n=len(trangThai[0])
    viTriOTrong=TimOTrong(trangThai)
    TrangThaiBatDau=(viTriOTrong,trangThai)
    hangDoi = HangDoiUuTien()
    hangDoi.push([TrangThaiBatDau],heuristic(trangThai))
    cacHanhDong = HangDoiUuTien()
    cacHanhDong.push([0],heuristic(trangThai))
    b= TrangThaiDich(trangThai)
    count=0
    while hangDoi:
        node = hangDoi.pop()
        node_action = cacHanhDong.pop()
        count+=1
        if KiemTraTrangThaiDich(node[0][1],b):
            print(','.join(node_action[1:]).replace(',',''))
            print('Số bước di chuyển: ',len(node_action) - 1,'Số trạng thái đã duyệt: ',count)
            break
        cost=len(node_action)
        for hanhDong in HanhDongHopLe(node[0][0], node[0][1]):
            viTriOTrongMoi, trangThaiMoi = CapNhatTrangThai(node[0][0], node[0][1], hanhDong)
            heur=heuristic(trangThaiMoi)
            hangDoi.push([(viTriOTrongMoi, trangThaiMoi)],heur*n*8/3+cost)
            cacHanhDong.push(node_action + [hanhDong[-1]],heur*n*8/3+cost)
    #de hien thi
    return node_action

'''''''''''''''''''hien thi'''''''''''''''''''''''''

def HienThiTrangThaiCapNhat(trangThai, diChuyen):
    n = len(trangThai[0])
    for x in range(n):
        for y in range(n):
            if trangThai[x][y]==0:
                xPlayer=x 
                yPlayer=y

    if diChuyen=='up':
        x1, y1 = xPlayer - 1, yPlayer + 0
    elif diChuyen=='right':
        x1, y1 = xPlayer + 0, yPlayer + 1
    elif diChuyen=='down':
        x1, y1 = xPlayer + 1, yPlayer + 0
    elif diChuyen=='left':
        x1, y1 = xPlayer + 0, yPlayer - 1

    
    trangThai[xPlayer][yPlayer] = trangThai[x1][y1]
    trangThai[x1][y1] = 0


def HienThiIndex(m,n):
    x=m//n
    y=m%n
    return x,y

top = tk.Tk()
top.title('8puzzle_game')



def HienThi(trangThai):
    n=len(trangThai[0])
    b=trangThai.reshape(n*n)
    hienThiTrangThai=[]
    for x in range(n*n):
        if b[x]!=0:
            value=b[x]
        else:
            value=""
        a0=tk.Button(text=value,font=("Helvetica",20,),height=3,width=7)
        hienThiTrangThai.append(a0)
    for x in range(n*n):
        x1, y1=HienThiIndex(x,n)
        hienThiTrangThai[x].grid(row=x1, column=y1)
    

def task():
    if len(move)!=0:
        HienThiTrangThaiCapNhat(trangThaiBanDau,move[0])
        del move[0]
        HienThi(trangThaiBanDau) 
        time.sleep(1)
        top.after(100,task)


Sample1=[1,2,3,7,4,6,5,0,8]
Sample2=[1,2,3,4,5,6,8,7,0]

trangThaiBanDau=DauVao(Sample1,3)


HienThi(trangThaiBanDau)
print(trangThaiBanDau)
time_start = time.time()
move=Astar(trangThaiBanDau)
time_end=time.time()
print('Thời gian giải: ',time_end-time_start,' second.')

del move[0]
top.after(100,task)
top.mainloop()