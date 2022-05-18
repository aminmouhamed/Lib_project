
def binery_search(list_x,x):
    medel = (len(list_x) - 1)//2
    print(list_x)
    if list_x[medel] == x :
        print(list_x[medel])
        return list_x[medel]
    else :
        
        if x > list_x[medel] :
            list_x = list_x[medel + 1:]

        elif x < list_x[medel] :
            list_x = list_x[ : medel]

    binery_search(list_x,x)
test_list = [1,2,3,4,5,6,7]
print(binery_search(test_list,1))


