#This code is in answer to 'Censor Dispenser' project on Code Academy. Having now seen their solution I realise mine assume there are no line breaks in the emails. Words in the banned lists must also not contain either an asterisk or a dollar sign.

#this function takes a phrase and replaces each character with an asterisk, and maintains spaces.

def replace_letters(censor_word): 
    new_word = ""
    for i in censor_word: 
        if i == " ":
            new_word += " "
        else: 
            new_word += "*"
    return new_word

#this function takes one word and censors it.

def censor(email,censor_word): 
    
#getting email and censored word in the same case.
    lower_email = email.lower()
    word_lower = censor_word.lower()
    
#making the orginal email a list of characters so it's mutable.
    email_list = list(email)
    
#finding how many times censored word in email
    count = lower_email.count(word_lower)  
    
#for each of those occurences, find the index the word starts and ends on and replace that slice of the original email with the result when the censored word is put in the 'replace letters' function.
    index_start = 0
    for i in range(0,count):
        index = lower_email.find(word_lower,index_start)
        index_end = index+len(censor_word)
        email_list[index:index_end] = replace_letters(censor_word)
        index_start = index_end     
        
#turn the list back into a string
    new_email = "".join(email_list)
    return new_email


#this function takes a list of words and censors all instances of any word in the list above a certain maximum number of instances (of any list word). Eg if maximum = 0 (as is default) all instances of words in the list will be censored.

def censor_list(email,censor_words,maximum=0):
    
    #getting email in lower case.
    lower_email = email.lower()
    
    #making the orginal email a list of characters so it's mutable.
    email_list = list(email) 
    
    indices = {}
    #each word in censored word list is made lower and then a dictionary is made, with indcies as keys and the censored word at that index as values.
    for word in censor_words: 
        word_lower = word.lower()
        count = lower_email.count(word_lower)  
        index_start = 0
        for i in range(0,count):
            index = lower_email.find(word_lower,index_start)
            index_end = index+len(word_lower)
            indices[index] = word_lower
            index_start = index_end
            
    #sort the dictionary so indices are in order, then censor any instances of censored words after the maximum number.       
    count = 0 
    for index in sorted(indices): 
        word = indices[index]
        index_end = index+len(word)
        if count >= maximum: 
            email_list[index:index_end] = replace_letters(word)
        else: 
            count += 1
            
    #and turns the list of characters back into a string.
    new_email = "".join(email_list)
    return new_email


#It would be a problem in 'censor_mega' (below) if the email used the asterisk and dollar sign (the characters I am using to censor words out with). This is because in censor_mega the code looks for those characters to work out which words have been censored by the censor_list function. The three functions below will be used in censor_mega to prevent this being a problem.

#this function checks the email for those 'censor characters' and keeps a track of them (and their index positions) in a ditctionary so we can put them back at the end.

def check_for_censor_characters(email): 
    censor_characters = ["*","$"]
    dic_of_index_lists = {}
    for thing in censor_characters: 
        count = email.count(thing)
        index_start = 0
        index_list = []
        for i in range(0,count):
            index = email.find(thing,index_start)
            index_list.append(index)
            index_start = index+1
        dic_of_index_lists[thing] = index_list    
    return dic_of_index_lists

#this function replaces those censor characters with something else.

def replace_censor_characters(email,dic): 
    if len(dic) >0: 
        email_list = list(email)
        for thing in dic:
            for i in dic[thing]:
                email_list[i] = "%"
        new_email = "".join(email_list)
    else: 
        new_email = email
    return new_email

#this function puts those censor characters back at their correct indices in the email.

def put_censor_characters_back(email,dic):
    if len(dic) >0:
        email_list = list(email)
        for thing in dic: 
            for i in dic[thing]: 
                email_list[i] = thing
        new_email = "".join(email_list)
    else: 
        new_email = email
    return new_email


#this function censors all bad words, all sad words after the first instance and then censors words either side of a censored word.
                  
def censor_mega(email,bad_words,sad_words):
    
    #this is checking for and replacing any asterisks and dollar signs.
    dic = check_for_censor_characters(email)
    print(dic)
    new_email = replace_censor_characters(email, dic)
    print(new_email)
    
    #this censors all bad words, all sad words after the first instance
    newer_email = censor_list(new_email,bad_words)
    new_newer_email = censor_list(newer_email,sad_words,1)
    
    #this turns the censored email into a list of words
    email_list = new_newer_email.split()
    
    #for each word in list check if it contains a censor character
    for i in range(len(email_list)):
        if "*" in email_list[i]:
            
            #if it does and it's not the first word then for each non-puntutation character in the word before it replace it with a dollar sign.
            if i > 0:
                for n in range(len(email_list[i-1])): 
                    if email_list[i-1][n] not in punctuation:
                        email_list[i-1] = email_list[i-1].replace(str(email_list[i-1][n]),"$") 
                        
            #if it does and it's not the last word then for each non-punctuation character in the word after it replace it with a dollar sign.
            if i < len(email_list) - 1:
                for n in range(len(email_list[i+1])): 
                    if email_list[i+1][n] not in punctuation:
                        email_list[i+1] = email_list[i+1].replace(str(email_list[i+1][n]),"$") 
                        
    #turn the list of words back into a string.                    
    final_email = (" ".join(email_list)).replace("$","*")
    
    #put any censor characters that were found in the original email, back
    final_final_email = put_censor_characters_back(final_email,dic)
    return final_final_email  

punctuation = [",", "!", "?", ".", ";", "/", "(", ")",";","-","&","@","#","%"]

bad_words = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithm", "her", "herself"]

sad_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressed", "concerning", "horrible", "horribly", "questionable"]


print(censor(email_one,"learning algorithms")
print(censor_list(email_two,bad_words)
print(censor_list(censor_list(email_three,bad_words),sad_words,maximum=1))
print(censor_mega(email_four,bad_words,sad_words))
      
