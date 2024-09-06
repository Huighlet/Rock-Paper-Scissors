import random

def player(prev_opponent_play):
    num_predictor = 27
    len_rfind = [20]
    limit = [10, 20, 60]
    beat = {"R": "P", "P": "S", "S": "R"}
    not_lose = {"R": "PPR", "P": "SSP", "S": "RRS"}  # 50-50 chance
    temp1 = {"PP": "1", "PR": "2", "PS": "3",
             "RP": "4", "RR": "5", "RS": "6",
             "SP": "7", "SR": "8", "SS": "9"}
    temp2 = {"1": "PP", "2": "PR", "3": "PS",
             "4": "RP", "5": "RR", "6": "RS",
             "7": "SP", "8": "SR", "9": "SS"}
    who_win = {"PP": 0, "PR": 1, "PS": -1,
               "RP": -1, "RR": 0, "RS": 1,
               "SP": 1, "SR": -1, "SS": 0}
    
    # Initialize state variables
    if not hasattr(player, "initialized"):
        player.initialized = True
        player.my_his = ""
        player.your_his = ""
        player.both_his = ""
        player.list_predictor = [""] * num_predictor
        player.length = 0
        player.score_predictor = [0] * num_predictor
        player.output = random.choice("RPS")
        player.predictors = [player.output] * num_predictor

    # Update predictors if the opponent has played before
    if prev_opponent_play:
        # Update predictors
        front = 0 if len(player.list_predictor[0]) < 5 else 1
        for i in range(num_predictor):
            result = "1" if player.predictors[i] == prev_opponent_play else "0"
            player.list_predictor[i] = player.list_predictor[i][front:5] + result

        # Update histories
        player.my_his += player.output
        player.your_his += prev_opponent_play
        player.both_his += temp1[prev_opponent_play + player.output]
        player.length += 1

        # Generate predictors
        for i in range(1):
            len_size = min(player.length, len_rfind[i])
            j = len_size

            # both_his
            while j >= 1 and player.both_his[player.length-j:player.length] not in player.both_his[0:player.length-1]:
                j -= 1
            if j >= 1:
                k = player.both_his.rfind(player.both_his[player.length-j:player.length], 0, player.length-1)
                player.predictors[0 + 6*i] = player.your_his[j+k]
                player.predictors[1 + 6*i] = beat[player.my_his[j+k]]
            else:
                player.predictors[0 + 6*i] = random.choice("RPS")
                player.predictors[1 + 6*i] = random.choice("RPS")

            # your_his
            j = len_size
            while j >= 1 and player.your_his[player.length-j:player.length] not in player.your_his[0:player.length-1]:
                j -= 1
            if j >= 1:
                k = player.your_his.rfind(player.your_his[player.length-j:player.length], 0, player.length-1)
                player.predictors[2 + 6*i] = player.your_his[j+k]
                player.predictors[3 + 6*i] = beat[player.my_his[j+k]]
            else:
                player.predictors[2 + 6*i] = random.choice("RPS")
                player.predictors[3 + 6*i] = random.choice("RPS")

            # my_his
            j = len_size
            while j >= 1 and player.my_his[player.length-j:player.length] not in player.my_his[0:player.length-1]:
                j -= 1
            if j >= 1:
                k = player.my_his.rfind(player.my_his[player.length-j:player.length], 0, player.length-1)
                player.predictors[4 + 6*i] = player.your_his[j+k]
                player.predictors[5 + 6*i] = beat[player.my_his[j+k]]
            else:
                player.predictors[4 + 6*i] = random.choice("RPS")
                player.predictors[5 + 6*i] = random.choice("RPS")

        for i in range(3):
            temp = ""
            search = temp1[(player.output + prev_opponent_play)]  # Last round
            for start in range(2, min(limit[i], player.length)):
                if search == player.both_his[player.length-start]:
                    temp += player.both_his[player.length-start+1]
            if temp == "":
                player.predictors[6 + i] = random.choice("RPS")
            else:
                collectR = {"P": 0, "R": 0, "S": 0}  # Take win/lose from opponent into account
                for sdf in temp:
                    next_move = temp2[sdf]
                    if who_win[next_move] == -1:
                        collectR[temp2[sdf][1]] += 3
                    elif who_win[next_move] == 0:
                        collectR[temp2[sdf][1]] += 1
                    elif who_win[next_move] == 1:
                        collectR[beat[temp2[sdf][0]]] += 1
                max1 = -1
                p1 = ""
                for key in collectR:
                    if collectR[key] > max1:
                        max1 = collectR[key]
                        p1 = key
                player.predictors[6 + i] = random.choice(p1)

        # Rotate 9-27
        for i in range(9, 27):
            player.predictors[i] = beat[beat[player.predictors[i-9]]]

        # Choose a predictor
        len_his = len(player.list_predictor[0])
        for i in range(num_predictor):
            sum = 0
            for j in range(len_his):
                if player.list_predictor[i][j] == "1":
                    sum += (j + 1) * (j + 1)
                else:
                    sum -= (j + 1) * (j + 1)
            player.score_predictor[i] = sum
        max_score = max(player.score_predictor)

        if max_score > 0:
            predict = player.predictors[player.score_predictor.index(max_score)]
        else:
            predict = random.choice(player.your_his)

        player.output = random.choice(not_lose[predict])
    
    # Logging for debugging
    print(f"Prev opponent play: {prev_opponent_play}")
    print(f"Output: {player.output}")
    print(f"Predictors: {player.predictors}")
    print(f"Score Predictor: {player.score_predictor}")
    
    return player.output
