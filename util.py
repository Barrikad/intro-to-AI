#Clumsy binary search for element/infimum/supremum
#bound = "inf" for greatest lower bound
#bound = "sup" for lowest greater bound
#bound = "eq" for equal element (i.e. gives index if it exists)
#Returns found element and its index in list if found
#Returns None otherwise
def binarySearch(list,element,bound):
    i = 0
    j = len(list) - 1
    while i <= j:
        if bound == "inf":
            mid = (i + j) // 2 + (i + j) % 2
        else:
            mid = (i + j) // 2 
        if list[mid] == element:
            return (element,mid)
        elif list[mid] < element and j != i:
            i = mid + (bound != "inf")
        elif list[mid] > element and j != i:
            j = mid - (bound != "sup")
        elif list[mid] < element and bound == "inf":
            return (list[mid],mid)
        elif list[mid] > element and bound == "sup":
            return (list[mid],mid)
        else:
            return None
    return None
        
#largest reasonable int
MAX_INT = 99999999