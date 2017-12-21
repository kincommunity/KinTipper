import praw
import config
import time
import Kin
import re


def bot_login():
    # Login with praw
    print "Logging in..."
    r = praw.Reddit(username = config.username,
                    password= config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "KinTipper Bot")
    print "Logged in!"

    return r


def getRelevantComments(r,lastReply):
    # Relevant comment contains "KinTipper", was posted after the last reply, and is not from me
    relevantComments = []

    print "Obtaining last 10 comments..."
    # Go over the last 10 comments
    for comment in r.subreddit('privbottest').comments(limit=10):
        if 'kintipper' in comment.body.lower() and comment.created_utc > lastReply and \
                        comment.author.name != config.username:
            relevantComments.append(comment)

    return relevantComments


def checkSyntax(comment):
    errormsg = None
    command = ''
    toUsername = ''
    amount = ''

    # Search for command (any string after !)
    try:
        command = re.search('(?<=!)\w+',comment.body.lower()).group(0)
    except Exception as e:
        errormsg = 'No command found'
        return errormsg, command, toUsername, amount
    # If the command is not recognized
    if command != 'tip' and command != 'register':
        errormsg = 'Invalid command: ' + command
        return errormsg, command, toUsername, amount

    # Check syntax for tip command
    if command == 'tip':
        # Search for username (any string after /u/)
        try:
            toUsername = re.search('(?<=/u/)\w+', comment.body.lower()).group(0)
        # re throws exception if you try to access the first index when it didnt find anything
        except Exception as e:
            errormsg = 'No username was found'
            return errormsg, command, toUsername, amount
        print 'Username found : ' + toUsername


        try:
            # Strip username to avoid numbers in username as amount
            amount = float(re.search('\d*\.?\d+', comment.body.lower().replace(toUsername,' ')).group(0))
        # re throws exception if you try to access the first index when it didnt find anything
        except Exception as e:
            errormsg = 'No Kin amount found'
            return errormsg, command, toUsername, amount
        if amount == 0:
            errormsg = 'Amount cant be 0'
            return errormsg, command, toUsername, amount

        print 'Amount found : ' + str(amount)

    return errormsg,command,toUsername,amount


def replyToComment(comment,msg):
    commentFormat = '\n\n ______________________________________ \n\n' \
                    'I am a bot, [What is this?](https://github.com/kinfoundation)\n\n' \
                    'Reply with \"KinTipper !register\" to use me too!'
    comment.reply(msg + commentFormat)
    return comment.created_utc


def sendRegisterDM(r,comment):
    # See if users have saved address
    with open('User Accounts', 'r') as myFile:
        Accounts = myFile.read().splitlines()
    myFile.close()
    if comment.author.name in Accounts:
        return False,'Already Registered'

    # Generate new wallet, and send the details to the user in a PM
    try:
        priv,addr = Kin.generateWallet()
        registrationMessage = 'Hey!, I see that you wanted to register for KinTipper, here are your new ethereum wallet details:\n\n' \
                              'Private Key: {}\n\n' \
                              'Address: {}\n\n' \
                              'THIS INFO IS ALSO STORED BY KINTIPPER (and Reddit), DO NOT SEND LARGE AMOUNTS OF MONEY TO THIS ADDRESS\n\n' \
                              '[How do I use this bot?](https://github.com/kinfoundation)'.format(priv,addr)
        r.redditor(comment.author.name).message('KinTipper Registration',registrationMessage)
        # Save the details for further use
        exportUser(comment.author.name,priv,addr)
    except Exception as e:
        return False,'Error'
    return True,'Worked'


def sendRegisterDMUnprompted(r,sender,reciver,amount):
    # Same as sendRegisterDM, but for a user that did not asked to register
    # Generate a new wallet, and send the details to the user
    try:
        priv,addr = Kin.generateWallet()
        registrationMessage = 'Hey {}, the user \"{}\" tried to send you {} Kin, however you do not have a KinTipper account' \
                              ' so I couldnt send them to you.' \
                              'I created a new ethereum wallet for you, to be used when ever you want to send/recive Kin via this bot:\n\n' \
                              'Private Key: {}\n\n' \
                              'Address: {}\n\n' \
                              'THIS INFO IS ALSO STORED BY KINTIPPER (and Reddit), DO NOT SEND LARGE AMOUNTS OF MONEY TO THIS ADDRESS\n\n' \
                              '[How do I use this bot?](https://github.com/kinfoundation)'\
            .format(reciver,sender,amount,priv,addr)
        r.redditor(reciver).message('KinTipper Registration',registrationMessage)
        # Save the details for further use
        exportUser(reciver,priv,addr)
    except Exception as e:
        return False
    return True


def tip(r,sendingName,recivingName,amount):
    # See if users have saved address
    with open('User Accounts','r') as myFile:
        Accounts = myFile.read().splitlines()
    myFile.close()

    if sendingName not in Accounts:
        return False,'No sending account'
    if recivingName not in Accounts:
        return False,'No receiving account'

    reciving = Accounts[Accounts.index(recivingName)+2] # Address of recicver
    sending = Accounts[Accounts.index(sendingName)+1] # Private of sender
    token = Kin.initSDK(sending)
    txID = Kin.sendTransaction(token,reciving,amount)
    if txID == 'Not enough Ether':
        return False,'Not enough Ether'
    if txID == 'Not enough Kin':
        return False,'Not enough Kin'

    tipPM = 'Here is the txID for your tip to {}\n\n https://ropsten.etherscan.io/tx/{}'.format(recivingName, txID)
    # Send transaction details to sending user
    r.redditor(sendingName).message('Your KinTipper transaction', tipPM)

    return True,'Worked'


def exportUser(name,priv,addr):
    with open('User Accounts','a') as myFile:
        myFile.write(name+'\n')
        myFile.write(priv+'\n')
        myFile.write(addr+'\n')
    myFile.close()


def run_bot(r,lastReply):
    # Get a list of comments
    relevantComments = getRelevantComments(r,lastReply)
    if len(relevantComments) == 0:
        print 'No Relevant comments'
        return lastReply
    print 'Found {} comments'.format(len(relevantComments))

    # Go over all comments
    for comment in relevantComments:
        # Check what the user wants from the bot
        syntaxResults = checkSyntax(comment)
        # If there is a syntax error, reply to the comment with the error
        if syntaxResults[0] != None:
            lastReply = replyToComment(comment,syntaxResults[0])

        # Handle registration request
        elif syntaxResults[1] == 'register':
            registerResponse = sendRegisterDM(r,comment)
            # If it was successful
            if registerResponse[0]:
                lastReply = replyToComment(comment,'Hey!, I sent you the registration instruction in a private message')
            elif registerResponse[1] == 'Already Registered':
                lastReply = replyToComment(comment,'You are already registered to KinTipper')
            else:
                lastReply = replyToComment(comment, 'Sorry, I couldnt register you, try again later :(')

        # Handle tip request
        else: # Command is tip
            tipResponse = tip(r, comment.author.name, syntaxResults[2], syntaxResults[3])
            # If it was successful
            if tipResponse[0]:
                lastReply = comment.reply('Hey!, I sent /u/{} {} Kin from you, I also sent you the txID in a PM'
                                          .format(syntaxResults[2],syntaxResults[3]))
            elif tipResponse[1] == 'Not enough Ether':
                lastReply = replyToComment(comment,'Sorry, there is not enough Ether in your account for gas')
            elif tipResponse[1] == 'Not enough Kin':
                lastReply = replyToComment(comment,'Sorry, there is not enough Kin in your account')
            elif tipResponse[1] == 'No sending account':
                lastReply = replyToComment(comment,'Hey, you dont have a KinTipper account yet, replay with \"KinTipper !register\" to open one')
            elif tipResponse[1] == 'No receiving account':
                # Send a registration PM to the user that didn't have an account
                sendRegisterDMUnprompted(r,comment.author.name,syntaxResults[2],syntaxResults[3])
                lastReply = replyToComment(comment,'Sorry, but /u/{} does not have a KinTipper account,'
                                                   ' I sent them a PM with instructions how to get one'.format(syntaxResults[2]))

    # lastReply holds the time of the last comment I replied to
    return lastReply


def main():
    startTime = time.time() #Current UNIX time

    r = bot_login()
    while True:
        # startTime gets the time of the last comment I replied to
        startTime = run_bot(r,startTime)
        print "Waiting for 20 seconds"
        time.sleep(20)



if __name__ == '__main__':
    main()