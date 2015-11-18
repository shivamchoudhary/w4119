def insertion_sort(Array):
    for i in range(1 ,len(Array)):
        j = i-1
        index = i
        while j>=0:
            if Array[index] <Array[j]:
                small_element = Array[index]
                big_element = Array[j]
                Array[j]=small_element
                Array[index]=big_element
            j = j-1
            index = index-1
    print Array 
Array = ['5','2','4','6','1','3']
insertion_sort(Array)

