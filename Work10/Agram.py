def the_cards():
    assigned = input("The cards are: ")
    cardsArray = assigned.split(" ")
    return cardsArray

def dealing_cards(cardsArray):
    
    # 确定翻面牌的花色和大小
    lead_card = cardsArray[0]

    if lead_card[0] == "T":
        lead_value = 10
    elif lead_card[0] == "J":
        lead_value = 11
    elif lead_card[0] == "Q":
        lead_value = 12
    elif lead_card[0] == "K":
        lead_value = 13
    elif lead_card[0] == "A":
        lead_value = 1
    else:
        lead_value = int(lead_card[0])
        
    if lead_card[1] == "C":
        lead_suit = 4
    elif lead_card[1] == "D":
        lead_suit = 3
    elif lead_card[1] == "H":
        lead_suit = 2
    elif lead_card[1] == "S":
        lead_suit = 1
    else:
        pass
        

    for cards in range(1,6):
        
        # 确定现在循环到的牌的花色和大小
        current_card = cardsArray[cards]
        
        if current_card[0] == "T":
            current_value = 10
        elif current_card[0] == "J":
            current_value = 11
        elif current_card[0] == "Q":
            current_value = 12
        elif current_card[0] == "K":
            current_value = 13
        elif current_card[0] == "A":
            current_value = 1
        else:
            current_value = int(current_card[0])
        
        if current_card[1] == "C":
            current_suit = 4
        elif current_card[1] == "D":
            current_suit = 3
        elif current_card[1] == "H":
            current_suit = 2
        elif current_card[1] == "S":
            current_suit = 1
        else:
            pass
        

        # 确定目前暂定出牌的大小
        if cards == 1:
            deal_card = current_card
        else:
            if deal_card[0] == "T":
                deal_value = 10
            elif deal_card[0] == "J":
                deal_value = 11
            elif deal_card[0] == "Q":
                deal_value = 12
            elif deal_card[0] == "K":
                deal_value = 13
            elif deal_card[0] == "A":
                deal_value = 1
            else:
                deal_value = int(deal_card[0])
            
            if deal_card[1] == "C":
                deal_suit = 4
            elif deal_card[1] == "D":
                deal_suit = 3
            elif deal_card[1] == "H":
                deal_suit = 2
            elif deal_card[1] == "S":
                deal_suit = 1
            else:
                pass
        
            
            #判断是否更改deal_card
            if current_suit == lead_suit == deal_suit:
                if current_value > lead_value and deal_value < lead_value:
                    deal_card = current_card
                else:
                    pass
            
            elif current_suit == lead_suit and deal_suit != lead_suit:
                deal_card = current_card
            
            elif current_suit != lead_suit and deal_suit == lead_suit:
                pass
            
            else:
                if current_value < deal_value:
                    deal_card = current_card
                elif current_value == deal_value:
                    if current_suit > deal_suit:
                        deal_card = current_card
                    else:
                        pass
                else:
                    pass
    

    return(deal_card)


def main():
    print("The must-play card is:", dealing_cards(the_cards()))


main()



            
            
