PI_ONE_THIRD = 1.047197 # 60 degree
PI_TWO_THIRD = 2.094395 # 120 degree
PI = 3.141592 # 180 degree
PI_FOUR_THIRD = 4.188790 # 240 degree
PI_FIVE_THIRD = 5.235987 # 300 degree
PI2 = 6.283185 # 360 degree

def rgb_to_hsv(p):
    (H, S, V) = 0, 0, 0

    r = p[0]/255
    g = p[1]/255
    b = p[2]/255

    maxC = max(r, g, b)
    minC = min(r, g, b)

    delta = maxC - minC

    if(delta == 0):
        H = 0
        S = 0
    else:
        if(maxC == r):
            H = (((g - b) / delta) % 6 ) * PI_ONE_THIRD
        elif(maxC == g):
            H = ((b - r) / delta + 2) * PI_ONE_THIRD
        elif(maxC == b):
            H = ((r - g) / delta + 4) * PI_ONE_THIRD

        S = delta / maxC
    V = max(r, g, b)

    result = [H, S, V]

    return result

def normalize(e):
    if(e < 0):
        return abs(e) % 1.0
    elif(e > 1):
        return (e % 1.0)
    else:
        return e
def normalizeH(e):
    if(e < 0):
        return abs(e) % PI2
    elif(e > PI2):
        return (e % PI2)
    else:
        return e

def hsv_to_rgb(p):
    r, g, b = 0, 0, 0

    H = normalizeH(p[0])
    S = normalize(p[1])
    V = normalize(p[2])

    C = V * S
    X = C * (1 - abs((H / PI_ONE_THIRD) % 2 - 1))
    m = V - C

    if(H < PI_ONE_THIRD): # 0 <= H < 60
        r, g, b = C, X, 0
    elif(PI_ONE_THIRD <= H and H < PI_TWO_THIRD): # 60 <= H < 120
        r, g, b = X, C, 0
    elif(PI_TWO_THIRD <= H and H < PI): # 120 <= H < 180
        r, g, b = 0, C, X
    elif(PI <= H and H < PI_FOUR_THIRD): # 180 <= H < 240
        r, g, b = 0, X, C
    elif(PI_FOUR_THIRD <= H and H < PI_FIVE_THIRD): # 240 <= H < 300
        r, g, b = X, 0, C
    elif(PI_FIVE_THIRD <= H and H < PI2): # 300 <= H < 360
        r, g, b = C, 0, X

    r, g, b = (r+m)*255, (g+m)*255, (b+m)*255

    result = [int(r), int(g), int(b)]
    return result

# 지정한 부분만 랜덤화
def modulate_hsv_plus(p, h = None, s = None, v = None):

    H = p[0]
    S = p[1]
    V = p[2]

    if(h != 0):
        H = H + h
    if(s != 0):
        S = S + s
    if(v != 0):
        V = V + v
    result = (H, S, V)
    return result

def modulate_hsv_assign(p, h = None, s = None, v = None):

    H = p[0]
    S = p[1]
    V = p[2]

    if(h != 0):
        H = h
    if(s != 0):
        S = s
    if(v != 0):
        V = v
    result = (H, S, V)
    return result