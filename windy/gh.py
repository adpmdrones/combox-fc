import bisect

# Gh altitude
#
#windy_gh = [1000, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300, 200, 150]
windy_gh = [150, 200, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000]


press = 927
print(press)

#gh = [ i for i in windy_gh if (press <= i and press >= i)]
gh = bisect.bisect(windy_gh, press)
print(gh)
print(windy_gh[gh - 13])
