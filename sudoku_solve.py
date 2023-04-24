import copy

class Sudoku:
    def __init__(self, level) -> None:
        self.level = level
        pass

def print_sudoku_res(sudoku_process):
    index_x = 0
    print_context = ''
    for item in sudoku_process:
        index_x += 1
        print_context += str(sudoku_process[item])
        if index_x % 3 == 0:
            print_context += ' | '
        if index_x % 9 == 0:
            print(print_context)
            print_context = ''

def check_square_only(sudoku_process):
    temp = 0
    for square_h in range(1,4):
        for square_s in range(1,4):
            square_check = {k:[0,(0,0)] for k in range(1,10)}
            for h in range(3):
                for s in range(3):
                    if len(sudoku_process[(square_h * 3 - h,square_s*3 - s)]) != 1:
                        for item in sudoku_process[(square_h * 3 - h,square_s*3 - s)]:
                            square_check[item][0] += 1
                            square_check[item][1] = (square_h * 3 - h,square_s*3 - s)
            for item in square_check:
                if square_check[item][0] == 1:
                    # print(square_check[item][1])
                    temp += 1
                    sudoku_process[square_check[item][1]] = [item]
    return temp

def check_line_only(sudoku_process):
    temp = 0
    for line_num in range(1,10):
        line_check = {k:[0,(0,0)] for k in range(1,10)}
        for column in range(1,10):
            if len(sudoku_process[(line_num,column)]) != 1:
                for item in sudoku_process[(line_num,column)]:
                    line_check[item][0] += 1
                    line_check[item][1] = (line_num,column)
        for item in line_check:
            if line_check[item][0] == 1:
                # print(line_check[item][1])
                temp += 1
                sudoku_process[line_check[item][1]] = [item]
    return temp

def check_column_only(sudoku_process):
    temp = 0
    for column_num in range(1,10):
        column_check = {k:[0,(0,0)] for k in range(1,10)}
        for line in range(1,10):
            if len(sudoku_process[(line,column_num)]) != 1:
                for item in sudoku_process[(line,column_num)]:
                    column_check[item][0] += 1
                    column_check[item][1] = (line,column_num)
        for item in column_check:
            if column_check[item][0] == 1:
                # print(column_check[item][1])
                temp += 1
                sudoku_process[column_check[item][1]] = [item]
    return temp

def match_rules(sudoku_process):
    indicator = 0
    zhishiqi = 0
    for item in sudoku_process:
        if len(sudoku_process[item]) == 1:
            temp_aim = sudoku_process[item][0]
            for x in range(1,10):
                if len(sudoku_process[(x,item[1])]) > 1 and temp_aim in sudoku_process[(x,item[1])]:
                    zhishiqi += 1
                    sudoku_process[(x,item[1])].remove(temp_aim)
                if len(sudoku_process[(item[0],x)]) > 1 and temp_aim in sudoku_process[(item[0],x)]:
                    zhishiqi += 1
                    sudoku_process[(item[0],x)].remove(temp_aim)
            heng = (item[0] - 1) // 3 + 1
            shu = (item[1] - 1) // 3 + 1
            for h in range(3):
                for s in range(3):
                    if len(sudoku_process[(heng*3-h, shu*3-s)]) > 1 and temp_aim in sudoku_process[(heng*3-h, shu*3-s)]:
                        zhishiqi += 1
                        sudoku_process[(heng*3-h, shu*3-s)].remove(temp_aim)
        else:
            indicator += 1
    return indicator, zhishiqi

def judge_sudoku(sudoku_process):
    # check line
    for line_num in range(1,10):
        line_check = {k:0 for k in range(1,10)}
        for column in range(1,10):
            if len(sudoku_process[(line_num,column)]) != 1:
                return False
            if line_check[sudoku_process[(line_num,column)][0]] == 0:
                line_check[sudoku_process[(line_num,column)][0]] = 1
            else:
                return False
    # check column
    for column_num in range(1,10):
        column_check = {k:0 for k in range(1,10)}
        for line in range(1,10):
            if len(sudoku_process[(line,column_num)]) != 1:
                return False
            if column_check[sudoku_process[(line,column_num)][0]] == 0:
                column_check[sudoku_process[(line,column_num)][0]] = 1
            else:
                return False
    # check square
    for square_h in range(1,4):
        for square_s in range(1,4):
            square_check = {k:0 for k in range(1,10)}
            for h in range(3):
                for s in range(3):
                    if len(sudoku_process[(square_h * 3 - h,square_s*3 - s)]) != 1:
                        return False
                    if square_check[sudoku_process[(square_h * 3 - h,square_s*3 - s)][0]] == 0:
                        square_check[sudoku_process[(square_h * 3 - h,square_s*3 - s)][0]] = 1
                    else:
                        return False

    return True
        
def judge_guess(guessed_list, sudoku_process_copy):
    for item in guessed_list:
        sudoku_process_copy[item[0]] = [item[1]]
    return judge_sudoku(sudoku_process_copy)

right_guess_list = []

def dfs(guess_list, guessed_list, sudoku_process):
    global right_guess_list
    if len(guess_list) == len(guessed_list) + 1:
        print('inside')
        sudoku_process_copy = copy.deepcopy(sudoku_process)
        if judge_guess(guessed_list, sudoku_process_copy):
            print('judge_guess_true')
            right_guess_list = guessed_list
        else:
            print('judge_guess_false')
        return
    for item in guess_list[len(guess_list)-len(guessed_list) - 1][1]:
        guessed_list.append([guess_list[len(guess_list)-len(guessed_list) - 1][0], item])
        dfs(guess_list, guessed_list, sudoku_process)

def guess_to_process(sudoku_process):
    global right_guess_list
    guess_list = [[item,sudoku_process[item]] for item in sudoku_process if len(sudoku_process[item]) > 1]
    print('guess_list')
    print(guess_list)
    print('guess_list')
    sudoku_process_copy = copy.deepcopy(sudoku_process)
    dfs(guess_list, [], sudoku_process_copy)
    if right_guess_list != []:
        for item in right_guess_list:
            sudoku_process[item[0]] = [item[1]]



    # while guess_list:
    #     guess_item = guess_list[0]
    #     for item in sudoku_process[guess_item]:
    #         sudoku_process_copy = copy.deepcopy(sudoku_process)
    #         sudoku_process_copy[guess_item] = [item]
    #         indicator = 1
    #         while indicator != 0:
    #             indicator, zhishiqi = match_rules(sudoku_process_copy)
    #             if zhishiqi == 0:
    #                 if judge_sudoku(sudoku_process_copy):
    #                     sudoku_process = sudoku_process_copy
    #                 else:
    #                     break
    #     guess_list.pop(0)
    #     pass
        
    #     for item in sudoku_process:
    #         if len(sudoku_process[item]) == 2:
    #             another_one = sudoku_process[item].pop(1)
    #             sudoku_process_copy = copy.deepcopy(sudoku_process)
    #             if judge_sudoku(sudoku_process_copy):
    #                 sudoku_process = sudoku_process_copy
    #             else:
    #                 sudoku_process[item] = [another_one]
    #             return 1
    # return 0

def solve_sudoku():
    level = 'hard'
    with open('sudoku_sample_' + level + '.txt') as f:
        a = f.read().split(',')
        # print(a)

    sudoku_map = {(a,b):0 for a in range(1,10) for b in range(1,10)}
    i = 0
    for item in sudoku_map:
        sudoku_map[item] = a[i]
        i += 1
    # print(sudoku_map)

    print('\n-----------------\n')
    sudoku_process = {k:[int(sudoku_map[k])] if sudoku_map[k] != '0' else [i for i in range(1,10)] for k in sudoku_map}
    print(sudoku_process)
    print('\n-----------------\n')
    indicator = 1
    zhishiqi = 1
    guess = 0
    while indicator != 0:
        if zhishiqi == 0:
            pass # find the only number in small square
            print('\n+_+_+_+_+_+_+\ncheck_square_only(sudoku_process)')
            if check_square_only(sudoku_process) == 0:
                print('\n+_+_+_+_+_+_+\ncheck_line_only(sudoku_process)')
                if check_line_only(sudoku_process) == 0:
                    print('\n+_+_+_+_+_+_+\ncheck_column_only(sudoku_process)')
                    if check_column_only(sudoku_process) == 0:
                        # need to go on to guess
                        guess = 1
                        break
            print('\n+_+_+_+_+_+_+\n')
        else:
            zhishiqi = 0

        indicator, zhishiqi = match_rules(sudoku_process)
        # print(indicator)
        # if indicator == 55:
        #     indicator = 0

    if guess == 1:
        pass
        # guess_to_process(sudoku_process)

    if judge_sudoku(sudoku_process):
        print('right answer')
    else:
        print('wrong answer')

    print_sudoku_res(sudoku_process)

if __name__ == '__main__':
    solve_sudoku()
