def paintleaves(m):
    for i in range(m):
        if(i == 10):
            print( ' '*(m-i) + '*'*( 2*i + 1-len( 'happy Christmas')) + 'happy Christmas'+ ' '*(m-i))
            continue
        if(i == 20):
            print( ' '*(m-i) + '*'*( 2*i + 1-len( 'happy Christmas')) +'happy Christmas'+ ' '*(m-i))
            continue
        if(i == m-1):
            print( ' '*(m-i) + 'happy Christmas'+ '*'*( 2*i + 1-len( 'happy Christmas')) + ' '*(m-i))
            continue   
        print(' '*(m-i) + '*'*(2*i + 1) + ' '*(m-i))   

def paintTrunk(n):
    for j in range (8 ):
       print(' '*(n - 5) + '*'*10 + ' '*(n - 5))


paintleaves(30)
paintTrunk(30)