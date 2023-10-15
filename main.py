import speech_recognition as sr
import pyttsx3
import openai as ai



# INITIALIZATION ---------------------------------------------------------------------------------


engine = pyttsx3.init()

#input fields

def input_fields():
    field = input("Enter technology to interview : ")
    interviewee_name=input("Enter your name : ")
    candidate_details=input("Enter other details : ")
    level_of_interview=input("Enter level of interview : ")
    gen = int(input("select gender(0-male, 1-female): "))
    predefined_questions = ['Could you be able to relocate to hyderabad ?', 'How much salary package do you expect']
    return field,interviewee_name,candidate_details,level_of_interview,gen,predefined_questions


field,interviewee_name,candidate_details,level_of_interview,gen,predefined_questions=input_fields()


if gen==0:
    name="Visku"
else:
    name="Lucy"



#---------conversation with chat bot--------

ai.api_key = "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"
context = "introduce yourself as "+name+". interview the user for a" + field + "job.Make sure that your message does not contain more than 1 questions and do not end the conversation until the interviewee is done ."+"Interviewee name is :"+interviewee_name+", additional details about the interviewee are"+candidate_details+". The level of interview questions must be "+level_of_interview+".ask more technical questions related to "+field+". include 1 practical question related to "+field +"and don't ask theory and practical question at same questions"
ctxt_msgs = [
    {"role": "assistant", "content": context}
]
eval_msgs = [
    {"role": "assistant",
     "content": "evaluate the answer of interviewee for the question of the interviewer and score it between 0 and 10"}
]


r = sr.Recognizer()
num_iter, a = 3, 0
sum1 = 0
reply = []
score1=[]
total=0

print("Could you please introduce yourself")

def speechtotext():
    t = input("Enter your reply : ")
    return t


def gptreply(msgs, msg, prnt=False):
    msgs.append({"role": "user", "content": msg})
    chat = ai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msgs)
    reply = chat.choices[0].message.content
    msgs.append({"role": "assistant", "content": reply})
    #if prnt:
        #print(reply)
    return reply


def score(ctxt_msgs, eval_msgs, field=None):
    print("evaluating score")
    ctxt_assist, ctxt_user, scores = [], [], []                  # init

    for i in ctxt_msgs:                                          # create - ctxt_assist, ctxt_user
        if i["role"] == "assistant":
            ctxt_assist.append(i["content"])
        else:
            ctxt_user.append(i["content"])
    del(ctxt_user[0], ctxt_user[-1])
    del(ctxt_assist[0], ctxt_assist[-1])

    for i in range(len(ctxt_user)):
        score, conv = [], "interviewer: " + ctxt_assist[i] + " interviewee: " + ctxt_user[i] + ". How well did interviewee answer, score him out of 10[show my just the score, I dont need any reason]"
        eval_msgs.append({"role": "user", "content": conv})         # collecting scores
        score_text = gptreply(eval_msgs, conv)

        for strng in score_text.split():
            try:
                score.append(float(strng))
            except:
                continue
        if score[0]:
            scr = score[0]
        else:
            scr = 0
        scores.append(scr)

    return sum(scores)/len(scores)


def data(ctxt_msgs):
    ctxt_assist, ctxt_user, scores = [], [], []
    for i in ctxt_msgs:
        if i["role"] == "assistant":
            ctxt_assist.append(i["content"])
        else:
            ctxt_user.append(i["content"])
    return ctxt_assist,ctxt_user


def repeat(msgs, say=False):
    print("shall I repeat the question?")
    ans = speechtotext()
    if ans == "yes":
        msgs.append({"role": "user", "content": "can you please repeat the question"})
        chat = ai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msgs)
        reply = chat.choices[0].message.content
        msgs.append({"role": "assistant", "content": reply})
        print(reply)
        if say:
            print(reply)
    else:
        print("Then please answer the question")



while 1:
    msg = speechtotext()
    if msg:
        if a > 0:
            if a == num_iter:

                conv = "person1: " + reply[0] + " person2: " + msg + ". How well did person2 answer, score him out of 10[show my just the score, I dont need any reason]"
                eval_msgs.append({"role": "user", "content": conv})
                score_text = gptreply(eval_msgs, conv, prnt=True)
                #print("evalation score: ", score_text)
                score1.append(score_text)
                response_list = []
                for i in range(len(predefined_questions)):
                    print(predefined_questions[i])
                    response = input("Enter your reply : ")
                    response_list.append(response)
                print("Thank you for attending the interview")

                break
            conv = "person1: " + reply[0] + " person2: " + msg + ". How well did person2 answer, score him out of 10[show my just the score, I dont need any reason]"
            eval_msgs.append({"role": "user", "content": conv})
            score_text = gptreply(eval_msgs, conv, prnt=True)
            #print("evalation score: ", score_text)
            score1.append(score_text)
        reply.append(gptreply(ctxt_msgs, msg, prnt=True))
    else:
        repeat(ctxt_msgs, say=True)
    print(reply[-1])
    a += 1

for ele in range(0, len(score1)):
    total = total + float(score1[ele])

print(total/len(score1))
print(score1)
ctxt_assistant,ctxt_user=data(ctxt_msgs)

print("response of predefined questions :")
print(response_list)
