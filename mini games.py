from tkinter import *
import socket
from threading import Thread
class Player:
    def __init__(self,cann):
        self.cann = cann
        self.player = self.cann.create_oval(100,100,200,200,fill="red")
    def move (self,e):
        if e.char == 'z' :
            self.cann.move(self.player, 0, -1)
        if e.char == 's' :
            self.cann.move(self.player, 0, 1)
        if e.char == 'd' :
            self.cann.move(self.player, 1, 0)
        if e.char == 'q' :
            self.cann.move(self.player, -1, 0)
        self.cann.update()
    def get_coords(self):
        coords = self.cann.coords(self.player)
        return coords
class Game(Tk):
    def __init__(self):
        super(Game, self).__init__()
        self.title("Multiplayer Game")
        self.geometry('500x500')
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
    def Main_Window(self):
        singel_player = Button(self,text="Singel Player",width = 50,height = 10,command = self.Singel_Player)
        Multi_Player = Button(self,text = "Multi Player",height = 10,width = 50,command = self.Multi_Player_Config)
        singel_player.grid(row = 0 , column = 0,padx = 80,pady = 50)
        Multi_Player.grid(row = 1 , column = 0)
        self.mainloop()
    def Singel_Player(self):
        self.clear_window()
        self.cann = Canvas(self, width=500, height=500)
        self.player1 = Player(self.cann)
        print(self.player1.get_coords())
        self.bind("<KeyPress>", self.player1.move)
        self.cann.grid(row = 0 ,column = 0)
        #self.mainloop()
    def Multi_Player_Config(self):
        self.clear_window()
        Label(self,text = "Enter ip : ").grid(row = 0,column = 0)
        self.ip = Entry(self,text = "Enter ip : ")
        self.ip.grid(row = 0 , column = 2)
        join = Button(self,text = "Join",command = self.test)
        creat = Button(self,text = "Creat",command = self.Multi_Player)
        join.grid(row = 1 , column = 0)
        creat.grid(row = 1 , column = 1)
    ################################################################################################
    ############################host configirations
    def Multi_Player(self):
        t = Thread(target=self.Creat_Server,args=())
        t.start()
        self.Singel_Player()
    def Creat_Server(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #print(str(socket.gethostbyname(socket.gethostname())))
        server.bind((str(socket.gethostbyname(socket.gethostname())),4444))
        server.listen(2)
        conn , addr = server.accept()
        player2 = Player(self.cann)
        print(f"connect with : {addr}")
        while True :
            server.send("test".encode("utf-8"))
            print(conn.recv(1024).decode("utf-8"))
            #player2.move(conn.recv(1024).decode())
            #self.bind("<KeyPress>",server.send)
        server.close()

    #############################################################################################
    ######################client configurations
    def Connect(self):
        player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player.connect((self.ip.get(),4444))
        player2 = Player(self.cann)
        while True :
            player.send("test".encode("utf-8"))
            print(player.recv(1024).decode("utf-8"))
            #self.player1.move(player.recv(1024).decode())
            #self.bind("<KeyPress>",player.send)

    """
    """
    def test(self):
        s = Thread(target=self.Connect,args=())
        s.start()

if __name__ == '__main__':
    Game().Main_Window()


