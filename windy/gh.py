# Gh altitude
#
windy_gh = [1000, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300, 200, 150]

press = 1018.20

gh = [ i for i in windy_gh if (press - i <= 25) or (press -i >= 25)]
print(gh)