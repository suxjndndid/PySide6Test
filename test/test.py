num = [1,2,3,4,5,6,7,8,9,10,11]
def page_test(page=0):
    for i in enumerate(num[page * 4:(page + 1) * 4]):
        print(i)

if __name__ == '__main__':
    page_test()
    print("*************************")
    page_test(2)