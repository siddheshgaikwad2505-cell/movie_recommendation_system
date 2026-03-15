# wapp to develop a chatbot using nltk

from nltk.chat import Chat

conv = [
	["hii|hello|hey",["how can i help you","yes","hii","hello"]],
	["contact|number",["9867583907"]],
	["location|address",["kalyan"]]
	]

chat = Chat(conv)
print("welcome--> SIDBOT and press q for quit")

while True:
	qts = input("-->")
	if qts == "q":
		break
	else:
		ans = chat.respond(qts)
		if ans is None:
			print("Sorry SIDBOT cant understand please contact--> 9867583907")
		else:
			print("SIDBOT-->",ans)

#p4.py --> photo in 10th Oct
# chatbot using cosine similarity