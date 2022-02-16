adminList = []
adminList.append(00000) #my discord id, removed
adminList.append(00000) #another discord id, also removed from the code

async def isAdmin(member):    
    if member.id in adminList:
        return True
    else:
        return False

#New Voice State Functions
async def userMuted(member):
    if member.voice.self_mute == True:
        return True
    else:
        return False

async def userDeaf(member):
    if member.voice.self_deaf == True:
        return True
    else:
        return False

async def userJoined(member, before, after):
    if before.channel == None and after.channel != None:
        return True
    else:
        return False


#Old Voice State Functions
'''async def userMuted(member, before, after):
    if before.self_mute == False and after.self_mute == True:
        return True
    else:
        return False


async def userUnmuted(member, before, after):
    if before.self_mute == True and after.self_mute == False:
        return True
    else:
        return False


async def userDeafened(member, before, after):
    if before.self_deaf == False and after.self_deaf == True:
        return True
    else:
        return False


async def userUndeafened(member, before, after):
    if before.self_deaf == True and after.self_deaf == False:
        return True
    else:
        return False


async def userLeft(member, before, after):
    if before.channel != None and after.channel == None:
        return True
    else:
        return False

async def userChangedChannel(member, before, after):
    if (before.channel != None and after.channel != None) and before.channel != after.channel:
        return True
    else:
        return False

async def wentAfk(member,before,after):
    if before.afk == False and after.afk == True:
        return True
    else:
        return False

async def leftAfk(member,before,after):
    if before.afk == True and after.afk == False:
        return True
    else:
        return False
'''