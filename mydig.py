import dns.query
import time
import datetime
import sys


# leaves only the A lines
def remove_aaaa(val):
    for line in val:
        if line.__contains__("AAAA"):
            val.remove(line)
    return val


def dig(domain, root):
    global name
    query = dns.message.make_query(domain, 1)
    val = dns.query.udp(query, root, 5)
    val = str(val)
    val = val.splitlines()

    if val[val.index(";ANSWER") + 1] == ";AUTHORITY":                                       # if we don't get the answer
        if val[val.__len__() - 1] != ";ADDITIONAL":                                         # if there are IPs given after ;ADDITIONAL
            remove_aaaa(val)
            if val[val.__len__() - 1] == ";ADDITIONAL":                                     # A doesn't exist in ;ADDITIONAL
                penultimate_line = val[val.index(";AUTHORITY") + 1]
                penultimate_line = penultimate_line.split(" ")
                new_name = penultimate_line[penultimate_line.__len__() - 1]
                dig(new_name, startServer)
            else:                                                                           # A exists in ;ADDITIONAL
                last_line = val[val.index(";ADDITIONAL") + 1]
                last_line = last_line.split(" ")
                dig(domain, last_line[last_line.__len__() - 1])
        else:                                                                               # no IP addresses exist in ;ADDITIONAL
            penultimate_line = val[val.index(";AUTHORITY") + 1]
            penultimate_line = penultimate_line.split(" ")
            new_name = penultimate_line[penultimate_line.__len__() - 1]
            dig(new_name, startServer)
    else:
        if not val[val.index(";ANSWER") + 1].__contains__(name):                            # answer of other server found
            temp_answer = val[val.index(";ANSWER") + 1]
            temp_answer = temp_answer.split(" ")
            next_ip = temp_answer[temp_answer.__len__() - 1]
            dig(name, next_ip)
        else:
            if val[val.index(";ANSWER") + 1].__contains__("CNAME"):
                cname_ans = val[val.index(";ANSWER") + 1]
                cname_ans = cname_ans.split(" ")
                cname = cname_ans[cname_ans.__len__() - 1]
                statements.append(val[val.index(";ANSWER") + 1])
                name = cname
                dig(cname, startServer)
            else:
                statements.append(val[val.index(";ANSWER") + 1])


statements = list()
name = sys.argv[1]
if name[name.__len__() - 1] != ".":
    question = name + ". In A"
    question = question.split(" ")
    print("QUESTION: SECTION")
    print('{0[0]:50}{0[1]:5}{0[2]}'.format(question) + "\n")
else:
    question = name + " In A"
    question = question.split(" ")
    print("QUESTION: SECTION")
    print('{0[0]:50}{0[1]:5}{0[2]}'.format(question) + "\n")
startServer = "192.203.230.10"

request_time = datetime.datetime.now()
t0 = time.time()
dig(name, startServer)
t1 = time.time()

total = t1 - t0
total = total * 1000
total = round(total)

print("ANSWER SECTION:")
for address in statements:
    address = address.split(" ")
    print('{0[0]:<40}{0[1]:10}{0[2]:5}{0[3]:10}{0[4]:15}'.format(address))
print("\nQUERY TIME: " + total.__str__() + " msec")
print("WHEN: " + request_time.__str__())
