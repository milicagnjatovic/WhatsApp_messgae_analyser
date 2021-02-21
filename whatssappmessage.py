import re
import sys
import matplotlib.pyplot as plt

if len(sys.argv)<=1:
    exit("Program expects name of file with messages as command line argument")
    
try:
    with open(sys.argv[1]) as f:
        sadrzaj = f.read()
except IOError:
    exit("Unknown file")

#print(sadrzaj)

ri = re.compile(r'(?P<date>\d+/\d+/\d+),\s*\d{2}:\d{2}\s*-\s*(?P<ime>[A-Za-z0-9žćčđš ]+)\s*:\s*(?P<poruka>.*?)\n', re.I | re.S)
people = {}
dates = {}
first_message = {}

m = ri.search(sadrzaj)

while m is not None:
    #print(m.group(), end = '\nX\n')
    #print(m.group("date") + "   " + m.group("ime") + "  " + m.group("poruka"))

    ime = m.group("ime")
    date = m.group("date")
    chars = len(m.group("poruka"))
    
    if(date in dates.keys()):
        dates[date] += 1
    else:
        dates[date] = 1
        if ime in first_message:
            first_message[ime].append(date)
        else:
            first_message[ime] = [date]
    
    if(ime in people.keys()):
        if(date in people[ime].keys()):
            people[ime][date]["msgs"] += 1
            people[ime][date]["chars"] += chars
        else:
            people[ime][date] = {
                "msgs":1,
                "chars": chars
                }
    else:
        people[ime] = {
            date:{ 
            "msgs":1,
            "chars": chars
            }
        }
    m = ri.search(sadrzaj, m.end());
    
person_messages ={}
person_chars ={}
for k in people.keys():
    print(k)
    msgs = 0
    chars= 0
    for date in people[k]:
        msgs += people[k][date]["msgs"]
        chars += people[k][date]["chars"]
    person_messages[k] = msgs
    person_chars[k] = chars
    print(str(msgs) + " " + str(chars))
    

cols = ('r', 'g', 'b', 'm', 'c')
colno = 0
colors = {}
for p in people.keys():
    colors[p] = cols[colno]
    colno = (colno+1)%len(cols)
    
clr = []
for p in person_messages.keys():
    clr.append(colors[p])

fig = plt.figure()
fig.set_figheight(8)
fig.set_figwidth(8)

ax1 = plt.subplot2grid(shape = (3,2), loc=(0,0))
ax1.bar(person_messages.keys(), person_messages.values(), color = clr)
ax1.set_title('Poslato poruka')
ax2 = plt.subplot2grid(shape = (3,2), loc=(0,1))
ax2.bar(person_chars.keys(), person_chars.values(), color = clr)
ax2.set_title('Poslato slova')

ax3 = plt.subplot2grid(shape = (3,2), loc=(1, 0), colspan = 2)
vals = {}
for d in dates.keys():
    vals[d] = -1
m = 0
for key in first_message.keys():
    i = 0;
    for date in first_message[key]:
        i += 1
        vals[date] = i
    ax3.scatter(vals.keys(), vals.values(), color = colors[key])
    colno = (colno+1)%len(colors)
    for date in first_message[key]:
        vals[date] = -1
    if i>m:
        m = i
ax3.set_ylim((1, m+2))
ax3.set_title('Datumi i ko je prvi pisao')

ax4 = plt.subplot2grid(shape = (3,2), loc=(2,0), colspan = 2)
ax4.plot(list(dates.keys()), dates.values())
ax4.set_title('Poruka po danima')

plt.tight_layout()
plt.show()
