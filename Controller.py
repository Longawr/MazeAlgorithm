import time
from tkinter import END, Button, Text, Tk, filedialog



class Gundam:
    def __init__(self):
        self.field = []
        self.result = []
        self.visited = []
        self.sum = 0
        self.maxSum = 0
        self.inputPath = 'resources\\input.txt'
        self.outputPath = 'resources\\output.txt'
        self.time = 0
        self.begin = (-1, -1)
        self.col = 0
        self.row = 0
        self.mode = False

    def open(self):
        self.refresh()
        self.field.clear()
        with open(self.inputPath, 'r') as f:
            line = f.readline().split(' ')
            self.row = int(line[0])
            self.col = int(line[1])
            self.begin = (int(line[2]), int(line[3]))
            for i in range(self.row):
                line =  f.readline().split(' ')
                temp = []
                temp.extend([int(num) for num in line if num != '\n'])
                self.field.append(temp)
        f.close()

    def refresh(self):
        self.visited.clear()
        self.result.clear()
        self.sum = 0
        self.maxSum = 0
        self.time = 0

    def save(self):
        with open(self.outputPath, 'w') as f:
            f.write(str(len(self.result)))
            f.write(' ')
            f.write(str(self.maxSum))
            f.write('\n')
            for i, j in self.result:
                f.write(str(self.field[i][j]))
                f.write(' >> ')
        f.close()

    def check(self, val):
        pointer = self.result if self.mode else self.visited
        if((val[0]) in range(len(self.field)) and (val[1]) in range(len(self.field[0]))):
            if(val not in pointer and (self.field[val[0]][val[1]] > 0)): 
                return True
        return False

    def backTracking(self, current):
        (x, y) = current
        count = 0
        self.visited.append((x, y))
        self.sum = self.sum + self.field[x][y]

        if self.check((x+1, y)):
            self.backTracking((x+1, y)) # dưới
            count +=1
        if  self.check((x, y+1)):
            self.backTracking((x, y+1)) # phải
            count +=1
        if self.check((x-1, y)):
            self.backTracking((x-1, y)) # trên
            count +=1
        if self.check((x, y-1)):
            self.backTracking((x, y-1)) # trái
            count +=1
        
        # nếu tới cuối đường
        if count == 0 and self.sum > self.maxSum:
            self.maxSum = self.sum
            self.result.clear()
            for i, j in self.visited:
                self.result.append((i, j))

        self.sum -= self.field[x][y]
        self.visited.remove((x, y))

    def greedy(self):
        #khởi tạo biến
        X=[-1,0,1,0]
        Y=[0,1,0,-1]
        (x, y) = notDeadEnd = deadEnd = self.begin
        while (x, y) not in self.result:
            self.result.append((x, y))
            maxValue1 = maxValue2 = 0
            availablePath = [0,0,0,0]
            for i in range(4):
                consider = (x+X[i], y+Y[i])
                #hàm check kiểm tra ô có thể đi được hay không
                if self.check(consider):
                    # kiểm tra và đếm ô xung quanh consider có đi được hay không
                    for j in range(4):
                        temp = (consider[0]+X[j], consider[1]+Y[j])
                        if self.check(temp):
                            availablePath [i]+= 1
                    # notDeadEnd lưu tọa độ có availablePath lớn hơn 0
                    if(availablePath[i] > 0):
                        if maxValue1 < self.field[consider[0]][consider[1]]:
                            notDeadEnd = consider
                            maxValue1 = self.field[consider[0]][consider[1]]
                    # deadEnd lưu tọa độ có availablePath bằng 0
                    elif maxValue2 < self.field[consider[0]][consider[1]]:
                        deadEnd = consider
                        maxValue2 = self.field[consider[0]][consider[1]]
            # nếu notDeadEnd có giá trị mới thì chọn nếu không thì chọn deadEnd
            (x, y) = notDeadEnd if (notDeadEnd != (x,y)) else deadEnd

    def start(self):
        self.refresh()
        start_time = time.time()
        self.greedy() if self.mode else self.backTracking(self.begin)
        end_time = time.time()
        self.time = end_time - start_time
        self.save()

    def input(self):
        screen = Tk()
        text = Text(screen, height = 10, width = 30)
        text.pack(side='top')
        file = open(self.inputPath, 'r')
        stuff = file.read()
        file.close()
        text.insert(END, stuff)

        btn = Button(screen, text = 'openfile', width = 5, command = lambda:self.inputbuttonPress(text)) 
        btn.pack(side='left')
        btn2 = Button(screen, text = 'save', width = 5, command = lambda:self.saveFile(text)) 
        btn2.pack(side='right')
        screen.mainloop()
    
    def output(self):
        top = Tk()
        text = Text(top, height = 3, width = 75)
        text.pack()
        btn = Button(top, text = 'choose output', width = 5, command = lambda:self.outputbuttonPress) 
        btn.pack()
        file = open(self.outputPath, 'r')
        stuff = file.read()
        file.close()
        text.insert(END, stuff)
        top.mainloop()

    def outputbuttonPress(self, text):
        fileName = filedialog.askopenfilename(initialdir=" ", filetypes=(("Text Files", "*.txt"), ))
        file = open(fileName, 'r')
        stuff = file.read()
        file.close()
        text.delete("1.0",END)
        text.insert(END, stuff)
        if fileName != '':
            self.outputPath = fileName
    
    def inputbuttonPress(self, text):
        fileName = filedialog.askopenfilename(initialdir=" ", filetypes=(("Text Files", "*.txt"), ))
        file = open(fileName, 'r')
        stuff = file.read()
        file.close()
        text.delete("1.0", END)
        text.insert(END, stuff)
        if fileName != '':
            self.inputPath = fileName

    def saveFile(self, text):
        stuff = text.get("1.0",'end-1c')
        file = open(self.inputPath, 'w')
        file.write(stuff)
        file.close()

def printStep(heith, gundam, int, font, color, screen, mess, score):

    distance = font.render( "score: {0:.2f}".format(score) + " (" + str(int) + "m)", True, color)
    if len(gundam.visited) != 0 or len(gundam.result) != 0:
        screen.blit(distance, (50, heith + 75))
    else:
        screen.blit(mess, (50 + 25, heith + 75))
    step = font.render("Elapsed time:{0:.5f}".format(gundam.time) + " sec", True, color)
    screen.blit(step, (50, heith + 105))

def surround(current, pos):
    X=[-1,0,1,0]
    Y=[0,1,0,-1]
    for i in range(4):
        if (current[0] +X[i], current[1] +Y[i]) == pos:
            return True
    return False