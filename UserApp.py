from VoteContract import VoteContract


if __name__ == '__main__':
    vote_contract = VoteContract()
    while True:
        my_choice = int(input("1. 투표하기\t2. 결과 확인\t3. 종료 >> "))
        if my_choice == 1:
            print("1. 기호 1번\t2. 기호 2번\n3. 기호 3번\t4. 기호 4번")
            vote_to = int(input("당신의 선택은? > "))
            complete= vote_contract.do_vote(vote_to)
            if complete:
                print("소중한 한 표 감사합니다.")
        elif my_choice == 2:
            winner = vote_contract.get_winner_name()
            if len(winner) != 0:
                print("%s이 최다 득표를 얻었습니다." % winner)
        elif my_choice == 3:
            print("프로그램을 종료합니다.")
            break
        else:
            print("유효하지 않은 입력입니다.")
