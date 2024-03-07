# correct answer:abc
var1 = input("input: ")
print(f"your input: {var1}")
# correct answer:xxx
var2 = input("input: ")
print(f"your input: {var2}")

#$VARIABLETEST test1
#$PROPERTY inputAnswers ["abc","xxx"]
#$TESTVAR var1
#$PROPERTY value abc
#$TESTVAR var2
#$PROPERTY value xxx

#yet not working:
##$STDOUTTEST test2
##$TESTVAR stdout
##$PROPERTY qualification startsWith
##$PROPERTY pattern "input: your input: ab"
