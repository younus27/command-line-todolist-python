import argparse
import sys
import os
from datetime import datetime 


def help():
	print("Usage :-")
	print('$ ./todo add "todo item"  # Add a new todo')
	print("$ ./todo ls               # Show remaining todos")
	print("$ ./todo del NUMBER       # Delete a todo")
	print("$ ./todo done NUMBER      # Complete a todo")
	print("$ ./todo help             # Show usage")
	print("$ ./todo report           # Statistics")

def add_element(text):
	if os.stat("todo.txt").st_size == 0:
		i=1
	else:
		with open('todo.txt', 'r') as fp:
		    Lines = fp.readlines()
		    i = len(Lines)+1
	#Add Item in Reverse Order -----------------------------
	with open('todo.txt', 'r+') as f:
	    content = f.read()
	    f.seek(0, 0)
	    f.write("["+str(i)+"] "+text.rstrip('\r\n') + '\n' + content)
	#-------------------------------------------------------

	#Update report.txt--------------------------------------
	with open('report.txt', 'r') as fp1:
		Lines = fp1.readlines()
		l = Lines[0].split(" ")
	with open('report.txt', 'w') as fp2:
		fp2.write(datetime.today().strftime('%Y/%m/%d')+" Pending : "+str( int(l[-4])+1) + " Completed : "+ l[-1]+"\n")
	print("Added todo:",text)
	#-------------------------------------------------------
	return



def delete_element(i):
	with open('todo.txt', 'r') as fp:
		Lines = fp.readlines()
	if i>len(Lines):
		print("Invalid Index")
		return

	# Delete Item and Maintain Order -----------------------
	text=[]
	for line in Lines:		
		if int(line.split(" ")[0][1])==i:
			pass
		else:
			text.append(" ".join(line.split("]")[1:])[1:])
	index=len(text)
	for j in range(len(text)):
		text[j] = "["+str(index-j)+"] "+text[j]
	with open('todo.txt', 'w') as fp:
		fp.truncate(0)
		for j in range(len(text)):
			fp.write(text[j])
	#-------------------------------------------------------

	#Update report.txt--------------------------------------
	with open('report.txt', 'r') as fp1:
		Lines = fp1.readlines()
		l = Lines[0].split(" ")
	with open('report.txt', 'w') as fp2:
		fp2.write(datetime.today().strftime('%Y/%m/%d')+" Pending : "+str(int(l[-4])-1) + " Completed : "+l[-1]+"\n")
	#-------------------------------------------------------
	print(f"Deleted todo #{i}")
	return


def done_element(i):
	with open('todo.txt', 'r') as fp:
		Lines = fp.readlines()
	if i>len(Lines):
		print(f"Error: todo #{i} does not exist.")
		return
	# Move Item to done.txt and Maintain Order ------------
	text=[]
	for line in Lines:		
		if int(line.split(" ")[0][1])==i:
			completed = " ".join(line.split("]")[1:])[1:]
		else:
			text.append(" ".join(line.split("]")[1:])[1:])
	index=len(text)
	for j in range(len(text)):
		text[j] = "["+str(index-j)+"] "+text[j]

	with open('todo.txt', 'w') as fp:
		fp.truncate(0)
		for j in range(len(text)):
			fp.write(text[j])
	with open("done.txt", 'a') as file1: 
		file1.write("x "+str(datetime.today().strftime('%Y/%m/%d'))+" "+completed)
	#-------------------------------------------------------
	
	#Update report.txt--------------------------------------
	with open('report.txt', 'r') as fp1:
		Lines = fp1.readlines()
		l = Lines[0].split(" ")
	with open('report.txt', 'w') as fp2:
		fp2.write(datetime.today().strftime('%Y/%m/%d')+" Pending : "+str(int(l[-4])-1)  + " Completed : "+str(int(l[-1])+1)+"\n")
	print(f"Marked todo #{i} as done.")
	#-------------------------------------------------------
	return






if __name__ == "__main__":

	#If File NOT Present, Create a File -------------------------------------------------
	with open('todo.txt', 'a') as fp:
		pass
	with open('todo.txt', 'a') as fp:
		pass
	try:
		with open('report.txt', 'r') as fp2:
			pass
	except:
		with open('report.txt', 'w') as fp2:
			fp2.write(datetime.today().strftime('%Y/%m/%d')+" Pending : 0 Completed : 0\n")
	#--------------------------------------------------------------------------------------


	try:
		parser =  argparse.ArgumentParser()
		parser.add_argument('get_args', type = str, help ="Enter an item")
		
		#Get arguments------------------------------------------
		args, unknown = parser.parse_known_args()
		#-------------------------------------------------------

		if args.get_args == "help" and unknown ==[]:
			help()



		elif args.get_args == "ls" and unknown ==[]:
			with open('todo.txt', 'r') as fp:
				Lines = fp.readlines()
			for line in Lines:
				print(line[:-1])



		elif args.get_args == "add":
			if len(unknown) ==0:
				print("missing one argument:    add STRING")
			elif len(unknown)>1:
				print(f"add takes only one argument, {len(unknown)} were given:    add STRING")
			else:
				add_element(unknown[0])



		elif args.get_args == "del":
			if len(unknown) ==0:
				print("missing one argument:    del NUMBER")
			elif len(unknown)>1:
				print(f"del takes only one argument, {len(unknown)} were given:    del NUMBER")
			else:
				try:
					i = int(unknown[0])
					delete_element(i)
				except:
					print(f"Error: todo #{i} does not exist. Nothing deleted.")



		elif args.get_args == "done":
			if len(unknown) ==0:
				print("missing one argument:    done NUMBER")
				try:
					with open('done.txt', 'r') as fp:
						Lines = fp.readlines()
					if len(Lines) == 0 :
						print("No Items Completed Yet...")
					else:
						print("\nItems Completed so far:")
						for line in Lines:
							print(line[:-1])
				except:
					with open("done.txt", 'a') as file1: 
						pass
			elif len(unknown)>1:
				print(f"done takes only one argument, {len(unknown)} were given:    done NUMBER")
			else:
				try:
					i = int(unknown[0])
					done_element(i)
				except:
					print(f"Error: todo #{i} does not exist.")



		elif args.get_args == "report" and unknown ==[]:
			with open('report.txt', 'r') as fp1:
				Lines = fp1.readlines()
			print(Lines[0])

		else:
			print("Invalid Command")
	except:
		#if no arguments passed -> print Help
		help()



