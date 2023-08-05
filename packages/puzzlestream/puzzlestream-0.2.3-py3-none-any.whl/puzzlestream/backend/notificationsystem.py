reactionMethods = []


def addReactionMethod(method):
    reactionMethods.append(method)


def newNotification(message):
    for m in reactionMethods:
        m(message)
