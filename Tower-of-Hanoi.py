import sys
sys.dont_write_bytecode = True
from tkinter import *
from turtle import TurtleScreen, RawTurtle
import functions

class Disc(RawTurtle):
    """Диск башни, объект RawTurtle на TurtleScreen."""
    def __init__(self, cv):
        RawTurtle.__init__(self, cv, shape="square", visible=False)
        self.pu()
        self.goto(-140,200)
    def config(self, k, n):
        self.hideturtle()
        f = float(k+1)/n
        self.shapesize(0.5, 1.5+5*f)
        self.fillcolor(f, 0, 1-f)
        self.showturtle()


class Tower(list):
    """Сабкласс для работы Ханойской башни"""
    def __init__(self, x):
        "Создаёт пустую башню. x - координат шпинделя"
        self.x = x
    def push(self, d):
        d.setx(self.x)
        d.sety(-70+10*len(self))
        self.append(d)
    def pop(self, y=90):
        d = list.pop(self)
        d.sety(y)
        return d


class HanoiEngine:
    """Запускает программу на созданном TurtleScreen."""
    def __init__(self, canvas, nrOfDiscs, speed, moveCntDisplay=None):
        """Устанавливает Canvas для воспроизведения, а также значения по умолчанию для
         количество дисков и скорость анимации.
         moveCntDisplay - это функция с 1 параметром, которая сообщает
         графическому интерфейсу программы подсчет хода"""
        self.ts = canvas
        self.ts.tracer(False)
        # отрисовка графики
        self.designer = RawTurtle(canvas, shape="square")
        self.designer.penup()
        self.designer.shapesize(0.5, 21)
        self.designer.goto(0,-80); self.designer.stamp()
        self.designer.shapesize(7, 0.5)
        self.designer.fillcolor('darkgreen')
        for x in -140, 0, 140:
            self.designer.goto(x,-5); self.designer.stamp()

        self.nrOfDiscs = nrOfDiscs
        self.speed = speed
        self.moveDisplay = moveCntDisplay
        self.running = False
        self.moveCnt = 0
        self.discs = [Disc(canvas) for i in range(10)]
        self.towerA = Tower(-140)
        self.towerB = Tower(0)
        self.towerC = Tower(140)
        self.ts.tracer(True)

    def setspeed(self):
        for disc in self.discs: disc.speed(self.speed)

    def move(self, src_tower, dest_tower):
        """Перемещает диск сверху на указанный шпиндель"""
        dest_tower.push(src_tower.pop())
        self.moveCnt += 1
        self.moveDisplay(self.moveCnt)

    def reset(self):
        """Перезапускает игру"""
        self.ts.tracer(False)
        self.moveCnt = 0
        self.moveDisplay(0)
        for t in self.towerA, self.towerB, self.towerC:
            while t != []: t.pop(200)
        for k in range(self.nrOfDiscs-1,-1,-1):
            self.discs[k].config(k, self.nrOfDiscs)
            self.towerA.push(self.discs[k])
        self.ts.tracer(True)

    def run(self):
        """Запуск игры
        Возвращает true, если игра окончена, если нет, то false"""
        self.running = True
        functions.play_hanoi(self, self.nrOfDiscs,
                             self.towerA, self.towerC, self.towerB)
        return True

class Hanoi:
    """Интерфейс для отображения элементов интерфейса программы"""

    def displayMove(self, move):
        """Функция для отображения текущего хода"""
        self.moveCntLbl.configure(text = "Ход:\n%d" % move)

    def adjust_nr_of_discs(self, e):
        """Функция установки количества дисков и веджета"""
        self.hEngine.nrOfDiscs = self.discs.get()
        self.reset()

    def adjust_speed(self, e):
        """Функция установки скорости, её виджета"""
        self.hEngine.speed = self.tempo.get() % 10
        self.hEngine.setspeed()

    def setState(self, STATE):
        """Управление состояниями"""
        self.state = STATE
        try:
            if STATE == "START":
                self.discs.configure(state=NORMAL)
                self.discs.configure(fg="black")
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=DISABLED)
                self.startBtn.configure(text="Начать", state=NORMAL)
            elif STATE == "RUNNING":
                self.discs.configure(state=DISABLED)
                self.discs.configure(fg="gray70")
                self.discsLbl.configure(fg="gray70")
                self.startBtn.configure(state=DISABLED)
            elif STATE == "DONE":
                self.discs.configure(state=NORMAL)
                self.discs.configure(fg="black")
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=NORMAL)
                self.startBtn.configure(text="start", state=DISABLED)
            elif STATE == "TIMEOUT":
                self.discs.configure(state=DISABLED)
                self.discs.configure(fg="gray70")
                self.discsLbl.configure(fg="gray70")
                self.resetBtn.configure(state=DISABLED)
                self.startBtn.configure(state=DISABLED)
        except TclError:
            pass

    def reset(self):
        """Изменяет состояние на START"""
        self.hEngine.reset()
        self.setState("START")

    def start(self):
        """Функция для кнопки Начать. Так же позволяет программе работать
        до её завершения."""
        if self.state == "START":
            self.setState("RUNNING")
            if self.hEngine.run():
                self.setState("DONE")


    def __init__(self, nrOfDiscs, speed):
        """Создание процесса работы Ханойской башни. Настройка интерфейса,
        установка состояния "START", и запуск mainloop()"""
        root = Tk()
        root.title("Ханойские башни")
        cv = Canvas(root,width=440,height=210, bg="gray90")
        cv.pack()
        cv = TurtleScreen(cv)
        self.hEngine = HanoiEngine(cv, nrOfDiscs, speed, self.displayMove)
        fnt = ("Arial", 12, "bold")
        # установка атрибутов количества дисков и скорость
        attrFrame = Frame(root)
        self.discsLbl = Label(attrFrame, width=7, height=2, font=fnt,
                              text="Диски:\n")
        self.discs = Scale(attrFrame, from_=1, to_=10, orient=HORIZONTAL,
                           font=fnt, length=75, showvalue=1, repeatinterval=10,
                           command=self.adjust_nr_of_discs)
        self.discs.set(nrOfDiscs)
        self.tempoLbl = Label(attrFrame, width=8,  height=2, font=fnt,
                              text = "   Скорость:\n")
        self.tempo = Scale(attrFrame, from_=1, to_=10, orient=HORIZONTAL,
                           font=fnt, length=100, showvalue=1,repeatinterval=10,
                           command = self.adjust_speed)
        self.tempo.set(speed)
        self.moveCntLbl= Label(attrFrame, width=5, height=2, font=fnt,
                               padx=20, text=" Ходы:\n0", anchor=CENTER)
        for widget in ( self.discsLbl, self.discs, self.tempoLbl, self.tempo,
                                                             self.moveCntLbl ):
            widget.pack(side=LEFT)
        attrFrame.pack(side=TOP)
        # управление: сброс, старт
        ctrlFrame = Frame(root) # содержит кнопки для управления
        self.resetBtn = Button(ctrlFrame, width=11, text="Сброс", font=fnt,
                               state = DISABLED, padx=15, command = self.reset)
        self.startBtn = Button(ctrlFrame, width=11, text="Начать", font=fnt,
                               state = NORMAL,  padx=15, command = self.start)
        for widget in self.resetBtn, self.startBtn:
            widget.pack(side=LEFT)
        ctrlFrame.pack(side=TOP)

        self.state = "START"
        root.mainloop()

if __name__  == "__main__":
    Hanoi(6,3)
