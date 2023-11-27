from everyday_task import EveryDayTask




if __name__ == '__main__':
    list = [(123,56),(123,58),(123,57),(123,25)]
    list1 = []
    while len(list) !=0:
        list1.append(list.pop(list.index(min(list))))
    # res = list1.sortd(reverse=True)
    res=sorted(list1,reverse=True)
    print(res)


    # c = False
    # while c:
    #     print(1)
    #     break
