import re


def cricket_algo():
    """
    It takes user input and calculates runs,wickets and overs
    :param: num_of_players
    :param: num_of_overs
    :param: players
    :return: string response of total runs/wickets/overs
    """
    # numbers of players in a team
    num_of_players = input("No. of players in the team: ")
    if int(num_of_players) == 0:
        error_msg = "Please enter any digit. Ex: 5"
        return error_msg

    # numbers of overs
    num_of_overs = input("No. of overs: ")
    if int(num_of_overs) == 0:
        error_msg = "Please enter any digit. Ex: 2"
        return error_msg

    # enter batting order wrt num_of_players
    batting_order = []
    for _ in range(num_of_players):
        players = input("Batting Order for the team: P{order digit} Ex: 'P1'/'P2'/'P3' ")
        if not re.search(r'\d+', players) or not re.search(r'[pP]', players):
            error_msg = "Please enter as directed: P{order digit} Ex: P1/P2/P3"
            return error_msg
        batting_order.append(players)

    # creating scoreboard for each player and by default first two players are opening batsmen
    players_scoreboard = create_scoreboard(batting_order)

    # get user input for run over-wise
    total_over_runs = []
    for _ in range(num_of_overs):
        runs_in_a_over = []
        for i in list(range(1, 7)):
            runs = str(input("Enter run for ball {}: ".format(i)))
            if runs.isdigit() or re.search(re.compile(r'[wW]+'), runs):
                runs_in_a_over.append(runs)
            else:
                error_msg = "Please enter either digit for run Ex: 1/2/3 or w for out"
                return error_msg

            # get on field players list
            on_field_players = player_status(players_scoreboard, "on_field_players")

            # check which player is batting now
            player = player_status(players_scoreboard, "batting_now")[0] if len(
                player_status(players_scoreboard, "batting_now")) > 0 else None

            # call player scoreboard to get updated
            if player in on_field_players:
                players_scoreboard = calculate_scoreboard(player, runs, players_scoreboard)

        # swap players' position after each over
        swap_players_after_every_over(players_scoreboard)

        print("\n")
        print(result_calculation(players_scoreboard, _))

    return "\n Inning ended \nFinal score \n" + result_calculation(players_scoreboard, num_of_overs)


def result_calculation(players_scoreboard,over):
    """
    :param players_scoreboard: dict
    :param over: int
    :return: string with total calculation
    """
    total = 0
    wicket = 0
    result = "\nScorecard for Team 1 \n" "Player-name Score"

    # calculate total scores
    for n, m in players_scoreboard.items():

        result += "\n" "{} {}".format(n+"*" if m.get("playing_now") == 1 else n, m.get('score'))
        total += m.get('score')

        # calculate total wickets
        if m.get('playing_now') == 3:
            wicket += 1

    return result + "\n" "Total {}/{}".format(total, wicket) + "\n" "Over {}".format(over)


def swap_players_after_every_over(players_scoreboard):
    """
    It exchanges value of currently active players on the fields
    :param players_scoreboard: dict
    :return: None
    """
    for n, m in players_scoreboard.items():
        if n in player_status(players_scoreboard, "on_field_players"):
            if m.get('batting_now') == 1:
                m['batting_now'] = 0
            else:
                m['batting_now'] = 1
    return


def player_status(player_data, status=None):
    """
    :param player_data: all player's dictionary data
    :param status: on_field_players/batting_now
    :return: list object containing response
    """
    on_field_players = []
    batting_player = []
    for i, j in player_data.items():
        if j.get("playing_now") and j.get("playing_now") == 1:
            on_field_players.append(i)
            if j.get("batting_now") and j.get("batting_now") == 1:
                batting_player.append(i)
    if status == "on_field_players":
        return on_field_players
    else:
        return batting_player


def calculate_scoreboard(player, run_data, player_order_data):
    """
    It takes runs data and ordering data as argument adn calculates total and individual score
    :param player:
    :param run_data:
    :param player_order_data:
    :return:
    """
    try:
        data = player_order_data.get(player)
        if run_data in ['w','W']:
            data['batting_now'] = 0
            data['playing_now'] = 3
            for n, m in player_order_data.items():
                if m['playing_now'] not in [1, 3]:
                    m['batting_now'] = 1
                    m['playing_now'] = 1
        else:
            data['score'] += int(run_data)
            if int(run_data) % 2 != 0:
                data['batting_now'] = 0
                for n, m in player_order_data.items():
                    if n in player_status(player_order_data, "on_field_players") and n != player:
                        m['batting_now'] = 1
            else:
                data['batting_now'] = 1
    except:
        print("Something went wrong, please provide correct data")

    return player_order_data


def create_scoreboard(players_ordering_data):
    """
    It takes players_ordering_data as argument and creates a scoreboard for each player wrt ordering.
    batting_now - who is facing the bowler's ball. 0 True or 1 False
    playing_now - who is not out and on the field now. 0 True or 1 False

    :param players_ordering_data:
    :return: a dictionary response
    """
    players_scoreboard = {}
    for i, j in enumerate(players_ordering_data):
        # first two players by default present on the field and first player is the opener
        if i == 0:
            players_scoreboard.update({j: {"score": 0, "batting_now": 1, "playing_now": 1}})
        elif i == 1:
            players_scoreboard.update({j: {"score": 0, "batting_now": 0, "playing_now": 1}})
        else:
            players_scoreboard.update({j: {"score": 0, "batting_now": 0, "playing_now": 0}})
    return players_scoreboard


if __name__ == "__main__":
    print(cricket_algo())
