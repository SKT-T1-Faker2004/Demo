import os
from Predictor import get_predicted_num
from Scraper import get_history_result
from MarPredict import predict_next
from Plot import plot

def main():
    os.chdir('/Users/ericzhou/Desktop/程序代码/Programming/Visual_Studio/Python/Projects/Lottery')
    file_name = 'data.csv'
    if not os.path.exists('data.csv'):
        maxi = input('How many pages of data to use(≤135) > ')
        get_history_result(file_name,maxi)
    else:
        choice = input('Use existing data? (y/n) > ')
        if choice == 'n':
            maxi = input('How many pages of data to use(≤135) > ')
            get_history_result(file_name,maxi)
        else:
            print('Using existing data......'); print()

    choice = input('1.Linear Regression\n2.Markov Chain\n3.Manual Work\nChoose which method to use> ')

    try:
        if int(choice) == 1:
            get_predicted_num(file_name, 'r1', 1, 'R1')
            get_predicted_num(file_name, 'r2', 2, 'R2')
            get_predicted_num(file_name, 'r3', 3, 'R3')
            get_predicted_num(file_name, 'r4', 4, 'R4')
            get_predicted_num(file_name, 'r5', 5, 'R5')
            get_predicted_num(file_name, 'r6', 6, 'R6')
            get_predicted_num(file_name, 'b1', 7, 'B1')
        elif int(choice) == 2:
            predict_next(file_name,'r1')
            predict_next(file_name,'r2')
            predict_next(file_name,'r3')
            predict_next(file_name,'r4')
            predict_next(file_name,'r5')
            predict_next(file_name,'r6')
            predict_next(file_name,'b1')
        else:
            plot(file_name)
    except ValueError:
        print('Please input a valid number!')

main()