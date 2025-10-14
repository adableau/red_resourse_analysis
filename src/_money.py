money = 8000
new_moneys = 0
new_benxi = 0

print(money * 15)


benxi = 0

for i in range(14):
    benxi += benxi * 0.04 + money
    print("-------" + str(i + 1))
    print(benxi)
for i in range(15, 29):
    benxi += benxi * 0.04
    print("-------" + str(i + 1))
    print(benxi)

licai=180000

print("------一次性本息--------")


benjin = 120000
lixi=0
for i in range(29):
    lixi += (benjin+lixi) * 0.04

    print(lixi)

print(lixi+benjin)
print(benjin*(1.04**29))


print("------亏损--------")
print(licai-benxi)


print(1000*1.045**2)