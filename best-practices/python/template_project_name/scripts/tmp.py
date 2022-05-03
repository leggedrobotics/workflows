ls = ["LOAD CONFIG", "CREAT EXPERIMENT FOLDER", "CREATE LOGGER", "CREAET NETWORK AND DATASET", "TRAINER SETUP",]
for s in ls:

    le = len(s)

    pre = int ((120-le - 4 -4 )/2)

    po = 120 - pre - le - 4 -4 

    print(pre, po)
    print ( "    " + "#"*pre+f"  {s}  " + "#"*po ) 