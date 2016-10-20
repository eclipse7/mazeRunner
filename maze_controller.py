def maze_controller(willie):

    mainCount = 0

    map1 = set([(0, 0)])
    position = (0, 0)
    rotation = (1, 0)

    def robot_turn_right():
        nonlocal willie, rotation
        right_rotation = {
            (1, 0): (0, 1),
            (0, -1): (1, 0),
            (-1, 0): (0, -1),
            (0, 1): (-1, 0)
        }
        rotation = right_rotation[rotation]
        willie.turn_right()

    def robot_turn_left():
        nonlocal willie, rotation
        left_rotation = {
            (0, 1): (1, 0),
            (1, 0): (0, -1),
            (0, -1): (-1, 0),
            (-1, 0): (0, 1)
        }
        rotation = left_rotation[rotation]
        willie.turn_left()

    def robot_go():
        nonlocal willie, rotation, position
        if willie.go():
            position = (position[0] + rotation[0], position[1] + rotation[1])
            return True
        else:
            return False

    def robot_set_rotation(new_rotation):
        nonlocal willie, rotation
        while rotation != new_rotation:
            robot_turn_right()

    def search_where_to_go():
        nonlocal rotation, position

        old_rotation = rotation[:]

        list_rotation = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        list_rotation_enabled = []

        for list in list_rotation:
            if (position[0] + list[0], position[1] + list[1]) not in map1:
                robot_set_rotation(list)
                if robot_go():
                    if position not in map1:
                        list_rotation_enabled.append(list)
                    robot_turn_right()
                    robot_turn_right()
                    robot_go()
                robot_set_rotation(old_rotation)

        return list_rotation_enabled

    # рекурсивная функция (дерево)
    def move_and_search(old_pos, old_rot):

        nonlocal mainCount
        mainCount = mainCount + 1

        nonlocal rotation, position, map1, willie
        old_position = old_pos[:]
        old_rotation = old_rot[:]

        list = []
        list.append(old_position)

        result = False

        while True:
            map1.add(position)
            list.append(position)
            if willie.found():
                result = True
                break
            list_enabled_move = search_where_to_go()[:]
            if len(list_enabled_move) == 1:
                print('one way')
                print(' ')
                robot_set_rotation(list_enabled_move[0])
                robot_go()
            else:
                break

        if result != True:
            if len(list_enabled_move) == 0:
                print('ex( go back')
                print(' ')
                for i in range(len(list)-1, 0, -1):
                    back_rotation = (list[i-1][0] - list[i][0], list[i-1][1] - list[i][1])
                    if back_rotation != (0, 0):
                        robot_set_rotation(back_rotation)
                        robot_go()
                robot_set_rotation(old_rotation)

            if len(list_enabled_move) > 1:
                print('more ways')
                print(' ')
                prev_pos = position[:]
                prev_rot = rotation[:]
                for enabled_move in list_enabled_move:
                    if result == False:
                        if (position[0] + enabled_move[0], position[1] + enabled_move[1]) not in map1:
                            robot_set_rotation(enabled_move)
                            robot_go()
                            # от 1 до 4 вызовов
                            result = move_and_search(prev_pos, prev_rot)

                if result == False:
                    print('ex( go back')
                    print(' ')
                    for i in range(len(list) - 1, 0, -1):
                        back_rotation = (list[i - 1][0] - list[i][0], list[i - 1][1] - list[i][1])
                        if back_rotation != (0, 0):
                            robot_set_rotation(back_rotation)
                            robot_go()
                    robot_set_rotation(old_rotation)

        return result

    # первый вызов рекурсивной функции
    move_and_search((0, 0), (1, 0))
    print('кількість рекурсивних викликів ', mainCount)
