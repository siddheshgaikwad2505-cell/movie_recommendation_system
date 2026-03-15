# wapp to develop the dictionary based chatbot

conv = {
	"hii":"hii",
	"hello" : "hello",
	"how are you":"i am fine",
	"where are you":"i am in kalyan",
	"what do you like":"i like playing",
	"contact":"9867583907"
	}

print("welcome--> SIDBOT and press q for quit")

while True:
	qts = input("-->")
	if qts == "q":
		break
	else:
		ans = conv.get(qts)
		if ans is None:
			print("Sorry SIDBOT cant understand please contact--> 9867583907")
		else:
			print("SIDBOT-->",ans)