from random import randint
import requests as req
from os import system
from Final_hand_detection import getInput
from time import sleep

system('cls')
print("_________________________Multiplayer Rock Paper Scissor Game_________________________")
print('\n\n\nEnter your choice : \n')
print('\n1. Create a room.\n\n2. Join a room.')
choice = int(input('\n'))

if choice == 1:
    system('cls')
    print("_________________________Multiplayer Rock Paper Scissor Game_________________________")
    appID = ''.join(['%s' % randint(0, 9) for _ in range(0, 6)])

    player1name = input("\n\nEnter your name : ")
    rounds = int(input("\nEnter number of rounds : "))
    winnercounter = rounds

    startAPI = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=start&appid=' + appID + '&pcon1=1&pname1=' + player1name + '&mround=' + str(
        rounds)
    req.get(startAPI)
    print("\nRoom ID : " + appID)

    player2confirmflag = 0
    player2name = ''

    while player2confirmflag == 0:
        print('.', end='')
        player2API = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchp2&appid=' + appID
        player2json = req.get(player2API).json()
        player2confirmflag = int(player2json['data'][0]['player2_confirm'])
        player2name = player2json['data'][0]['player2_name']

    print("\n\nSecond Player :", player2name)

    print('\n\nSelect your choice : \n\n1. Rock  2. Paper 3. Scissors\n\n')
    i = 1
    tempLst = {'1': 'Stone', '2': 'Paper', '3': 'Scissor'}
    while True:
        print('Enter your ' + str(i) + ' choice : ')
        move = getInput()
        print(tempLst[move])
        player1moveAPI = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=movep1&appid=' + appID + '&round=' + str(
            i) + '&optp1=' + move
        req.get(player1moveAPI)

        player2moved = 0
        while player2moved == 0:
            nextMoveAPI = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchmove&appid=' + appID + '&round=' + str(
                i)
            waitMoveJson = req.get(nextMoveAPI).json()
            player2moved = int(waitMoveJson['data'][0]['p2_move'])

        i += 1
        rounds -= 1
        if rounds == 0:
            break

    winnerAPI = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=showall&appid=' + appID
    winnerjson = req.get(winnerAPI).json()

    winnerlst = list()
    for k in range(winnercounter):
        winnerlst.append(int(winnerjson['data'][k]['winner']))

    p1_points = winnerlst.count(1)
    p2_points = winnerlst.count(2)

    if p1_points > p2_points:
        print('\n' + player1name + ' is Winner !')
    elif p1_points < p2_points:
        print('\n' + player2name + ' is Winner !')
    elif p1_points == p2_points:
        print('\n\nTie between ' + player1name + " and " + player2name + ".")

    system('pause')

elif choice == 2:
    system('cls')
    print("_________________________Multiplayer Rock Paper Scissor Game_________________________")
    winner = {(1, 1): 3, (2, 2): 3, (3, 3): 3, (1, 2): 2, (1, 3): 1, (2, 1): 1, (2, 3): 2, (3, 1): 2, (3, 2): 1}
    p1_move = 0
    p2_move = 0
    appID = input('\n\nEnter Room ID : ')
    player2name = input("\nEnter your name : ")
    player1API = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchp1&appid=' + appID + '&pcon2=1&pname2=' + player2name
    player1json = req.get(player1API).json()
    player1name = player1json['data'][0]['player1_name']
    print('\n\nFirst Player : ', player1name)

    rounds = int(player1json['data'][0]['max_round'])
    winnercounter = rounds

    while True:
        try:
            x = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchmove&appid=' + appID + '&round=' + str(
                1)
            y = req.get(x).json()
            p1_move = int(y['data'][0]['p1_move'])
            break
        except:
            pass

    print('\n\nSelect your choice : \n\n1. Rock  2. Paper 3. Scissors\n\n')
    i = 1
    tempLst = {'1': 'Stone', '2': 'Paper', '3': 'Scissor'}
    while True:
        temp3 = 0
        while temp3 == 0:
            temp1 = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchmove&appid=' + appID + '&round=' + str(
                i)
            temp2 = req.get(temp1).json()
            # print(temp2)
            try:
                p1_move = int(temp2['data'][0]['p1_move'])
                temp3 = int(temp2['data'][0]['p1_move'])
            except:
                temp3 = 0
        print('Enter your ' + str(i) + ' choice : ')
        sleep(2)
        move = getInput()
        print(tempLst[move])
        p2_move = int(move)
        player2moveAPI = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=movep2&appid=' + appID + '&round=' + str(
            i) + '&optp2=' + move + '&winner=' + str(winner[(p1_move, p2_move)])
        req.get(player2moveAPI)

        player1moved = 0
        while player1moved == 0:
            nextMoveAPI = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchmove&appid=' + appID + '&round=' + str(
                i)
            waitMoveJson = req.get(nextMoveAPI).json()
            player1moved = int(waitMoveJson['data'][0]['p1_move'])

        i += 1
        rounds -= 1
        if rounds == 0:
            break

    winnerAPI = 'http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=showall&appid=' + appID
    winnerjson = req.get(winnerAPI).json()

    winnerlst = list()
    for k in range(winnercounter):
        winnerlst.append(int(winnerjson['data'][k]['winner']))

    p1_points = winnerlst.count(1)
    p2_points = winnerlst.count(2)

    if p1_points > p2_points:
        print('\n' + player1name + ' is Winner !')
    elif p1_points < p2_points:
        print('\n' + player2name + ' is Winner !')
    elif p1_points == p2_points:
        print('\n\nTie between ' + player1name + " and " + player2name + ".")

    system('pause')

else:
    print("Invalid Choice !")
    system('pause')
