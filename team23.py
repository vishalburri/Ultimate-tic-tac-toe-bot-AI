import random
import copy
class Player23():
	"""docstring for Player23"""
	def __init__(self):
		self.bcount1=0
		self.fde=4
		self.cntp=0
		self.cnto=0
		self.count=0
		self.num=0
		self.cnt1=0
		self.bcount2=0
		self.cnt2=0

	def move(self, board, old_move, flag):
		temp_board = copy.deepcopy(board)
		bs = board.block_status
		self.cntp=0
		self.cnto=0
		self.num+=1
		for i in range(4):					
			for j in range(4):
				if bs[i][j] == 'x':
					self.cntp += 1
				if bs[i][j] == 'o':
					self.cnto += 1
		if self.cnto-self.cntp>=5 or self.num>75 or self.cntp>=4:
			self.fde=4

		nextmove = self.minimax(temp_board,old_move,True,flag,0,-100000,100000,-1,-1)
		return (nextmove[1],nextmove[2])
	
	def minimax(self,tempboard,old_move,maxplayer,flag,depth,alpha,beta,goodrow,goodcol):
		utility=0
		if self.fde == depth:
			if flag=='x':
				oppflag='o'
			else:	
				oppflag='x'
			checkwin=0	
			utility = self.get_utility(tempboard,flag)
			utility = round(utility,4)
			
			opputility = self.get_utility(tempboard,oppflag)
			opputility=round(opputility,4)
			checkwin=1
			if utility==1:
				opputility=0
			elif opputility==-1:
				utility=0
				
			return (utility-opputility,goodrow,goodcol)
		else:
			moves=tempboard.find_valid_move_cells(old_move)
			if depth == 0:
				if len(moves) > 16:
					self.fde = min(self.fde, 3)
			

			checkwin=0		
			if len(moves) == 0:
				utility = self.get_utility(tempboard,flag)
				if flag=='x':
					oppflag='o'
				else:
					oppflag='x'
				checkwin=1	

				opputility = self.get_utility(tempboard,oppflag)

				utility = round(utility,4)
				opputility=round(opputility,4)
				self.fde = max(depth, 4)
				checkwin=0
				if utility==1:
					opputility=0
				elif opputility==-1:
					utility=0
					
				return (utility-opputility, old_move[0], old_move[1])
			for move in moves:

				tempboard.board_status[move[0]][move[1]]=flag

				lol= tempboard.update(old_move,move,flag)
				checkwin=1
			

				if maxplayer:
					if flag=='o':
						flag='x'
					else:
						flag='o'

					util=self.minimax(tempboard,move,False,flag,depth+1,alpha,beta,goodrow,goodcol)
					
					utility = round(util[0],4)
					if utility > alpha:
						alpha = utility
						goodrow = move[0]
						goodcol = move[1]
				else:
					if flag =='o':
						flag='x'
					else:
						flag='o'
		
					util=self.minimax(tempboard,move,True,flag,depth+1,alpha,beta,goodrow,goodcol)
					utility = round(util[0], 4)
					if utility < beta:
						checkwin=1
						beta = utility
						goodrow = move[0]
						goodcol = move[1]

				tempboard.board_status[move[0]][move[1]]='-'	

				if alpha >= beta:
					checkwin=0
					break
			if depth == 0:
				if goodrow == -1 or goodcol == -1:
					goodrow = moves[0][0]
					goodcol = moves[0][1]
			if maxplayer:
				checkwin=1
				return (alpha, goodrow, goodcol,len(moves))
			else:
				return (beta, goodrow, goodcol,len(moves))  	

	def get_utility(self,tempboard,flag):
		utilityvalues=[0 for i in range(16)]
		gain=0
	
		for i in range(16):
			utilityvalues[i]=self.calculateutility(tempboard,i,flag)
		for i in range(4):
			gain+=self.createboardh(utilityvalues,i,4+i,8+i,12+i)	
		for j in range(4):
			gain+=self.createboardh(utilityvalues,j*4,j*4+1,j*4+2,j*4+3)	
		
		gain+=self.createboardh(utilityvalues,0,1*4+1,2*4+2,3*4+3)	
		gain+=self.createboardh(utilityvalues,3,6,9,12)	
		return gain
	def calculateutility(self,tempboard,blockno,flag):
		gain=0
		initx = blockno/4
		inity = blockno % 4
		initx *= 4
		inity *= 4
		for i in range(initx,initx+4):
			currp = 0
			curro = 0
			currd  =0
			for j in range(inity,inity+4):
				if tempboard.board_status[i][j]==flag:
					currp+=1
				elif tempboard.board_status[i][j]!='-':
					currp-=10
			if currp==1:
				gain+=1
			if currp==2:
				gain+=10
			if currp==3:
				gain+=80
			if currp==4:
				gain+=500				
		for j in range(inity,inity+4):
			currp = 0
			curro = 0
			currd  =0
			for i in range(initx,initx+4):
				if tempboard.board_status[i][j]==flag:
					currp+=1
				elif tempboard.board_status[i][j]!='-':
					currp-=10
			if currp==1:
				gain+=1
			if currp==2:
				gain+=10
			if currp==3:
				gain+=80
			if currp==4:
				gain+=500
		currp=0
		curro=0
		currd=0

		for i in range(0,4):
			if tempboard.board_status[initx+i][inity+i]==flag:
				currp+=1
			elif tempboard.board_status[initx+i][inity+i]!='-':
				currp-=10
			if currp==1:
				gain+=1
			if currp==2:
				gain+=10
			if currp==3:
				gain+=80
			if currp==4:
				gain+=500
		currp=0
		curro=0
		currd=0

		for i in range(0,4):
			if tempboard.board_status[initx+i][inity+3-i]==flag:
				currp+=1
			elif tempboard.board_status[initx+i][inity+3-i]!='-':
				currp-=10
			if currp==1:
				gain+=1
			if currp==2:
				gain+=10
			if currp==3:
				gain+=80
			if currp==4:
				gain+=500
		if gain>=500:
			gain=500
		gain=gain*1.0/500
		return gain

	def createboardh(self,utilityvalues,i,j,k,l):
		h=0
		temp=utilityvalues[i]+utilityvalues[j]+utilityvalues[k]+utilityvalues[l]
		flag=0
		if(temp<0):
			flag=1
		p_80=0
		p_20=0
		lose=0
		u_80=0
		u_20=0
		p_0=0
		n_0=0
		n_20=0
		n_80=0	
		win=0
		temp = utilityvalues[i] + utilityvalues[j] + utilityvalues[k] + utilityvalues[l]
		a=[i,j,k,l]
		b=[]

		for q in a:
			b.append(utilityvalues[q])
		pos=0
		for i in b:
			if i ==-1:
				lose+=1
			elif i==1:
				win+=1
			elif i > 0.15:
				p_80+=1
			elif i>0.15:
				u_20+=1
				
			elif i >= 0.08:
				p_20+=1
			elif i > 0:
				p_0 += 1
			elif i < -0.15:
				n_80 += 1
			elif i<-0.15:
				u_80+=1
				
			elif i <= -0.08:
				n_20 += 1
			elif i< 0:
				n_0 += 1
			if(p_80==3 and n_20==1):
				temp=temp*0.8
			if(p_80==3 and n_80==1):
				temp=temp*0.9
			if(u_20==2 and u_80==1):
				u_20=1
				
			if(p_80==3 and lose==1):
				temp=temp*0.5
			if(p_20==3 and n_80==1):
				temp=temp*0.9
			if(p_20==3 and lose==1):
				temp=temp*0.3
			if(u_20==3 and lose==1):
				lose=1
					


			if(win==3 and n_80==1):
				temp=temp*0.3
			if(win==3 and lose==1):
				temp=0

			if(n_80==3 and p_80==1):
				temp=temp*1
			if(n_80==3 and win==1):
				temp=temp*0.4
			if(u_80==3 and win==1):
				win=1
				

			if(n_20==3 and p_80==1):
				temp=temp*0.8
			if(n_20==3 and win==1):
				temp=temp*0.6

			if(lose==3 and win==1):
				temp=0
			if(lose==3 and p_80==1):
				temp=temp*0.3
			if(lose==3 and u_20==2):
				lose=3
				


			if(win==1 and p_0==3):
				temp=temp*0.4
			elif (p_80==1 and p_0==3):
				temp=temp*0.7
    #    elif(p_80==1 and p_20==2):


			if(lose==1 and n_0==3):
				temp=temp*0.4
			elif (n_80==1 and n_0==3):
				temp=temp*0.7

			if(flag==1):
				temp=-temp
			if temp < 0.32:
				h += temp
			elif temp >= 0.32 and temp <= 0.79:
				h += ( (temp -0.24) *12) + 1
			elif temp >= 0.79 and temp <4:
				h = (temp-0.79)*90 + 10
			elif temp>=4:
				h +=1000
			if(flag==1):
				return -h
			else:
				return h	




	




