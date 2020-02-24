import dns.query
import time
import sys

name = "www.cnn.com" #sys.argv[1]
print("Domain Name: " + name)
startServer = "192.203.230.10"


# leaves only the A lines
def remove_aaaa(val):
    for line in val:
        if line.__contains__("AAAA"):
            val.remove(line)
    return val


def dig(domain, root):
    query = dns.message.make_query(domain, 1)
    val = dns.query.udp(query, root, 5)
    val = str(val)
    val = val.splitlines()

    if val[val.index(";ANSWER") + 1] == ";AUTHORITY":                   # if we don't get the answer
        if val[val.__len__() - 1] != ";ADDITIONAL":                     # if there are IPs given after ;ADDITIONAL
            remove_aaaa(val)
            if val[val.__len__() - 1] == ";ADDITIONAL":                 # A exists in ;ADDITIONAL
                penultimate_line = val[val.__len__() - 2]
                penultimate_line = penultimate_line.split(" ")
                new_name = penultimate_line[penultimate_line.__len__() - 1]
                dig(new_name, startServer)
            else:                                                       # A doesn't exist in ;ADDITIONAL
                last_line = val[val.__len__() - 1]
                last_line = last_line.split(" ")
                dig(domain, last_line[4])
        else:                                                           # no IP addresses exist in ;ADDITIONAL
            penultimate_line = val[val.__len__() - 2]
            penultimate_line = penultimate_line.split(" ")
            new_name = penultimate_line[penultimate_line.__len__() - 1]
            dig(new_name, startServer)
    else:
        print(val[val.index(";ANSWER") + 1])


t0 = time.time()
dig(name, startServer)
t1 = time.time()
total = t1 - t0
total = total * 1000

print(total)

# query = dns.message.make_query(name, 1)
# val = dns.query.udp(query, startServer, 5)
# print(val)
# val = str(val)
# val = val.splitlines()
# lastLine = val[val.__len__() - 1]
# lastLine = lastLine.split(" ")
# nextName = lastLine[0]
# nextIP = lastLine[4]
# print(nextName)
# print(nextIP)

# query = dns.message.make_query(name, 1)
# val = dns.query.udp(query, startServer)
