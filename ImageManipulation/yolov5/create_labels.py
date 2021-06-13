# Creates labels in YOLOv5 format (? needs verification)
input_file = "/home/awfulwaffle/Downloads/FullIJCNN2013/FullIJCNN2013/labels.txt"

labels = []
with open(input_file) as file:
    lines = file.readlines()

for line in lines:
    right = line.split("=")[1]
    label = right.split("(")[0]
    label = label[1:]
    label = label [:-1]
    labels.append(label)

print("[", end="")
for label in labels:
    label_ = "'" + label + "'"
    if label != labels[len(labels) - 1]:
        print(label_, end=",")
    else:
        print(label_,end="")
print("]")
print("nc:", len(labels))