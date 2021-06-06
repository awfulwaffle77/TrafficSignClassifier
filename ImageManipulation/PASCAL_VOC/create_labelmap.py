OUTPUT_FILE  = "labelmap.pbtxt"

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

# print("[", end="")
# for label in labels:
#     label_ = "'" + label + "'"
#     if label != labels[len(labels) - 1]:
#         print(label_, end=",")
#     else:
#         print(label_,end="")
# print("]")
# print("nc:", len(labels))

fout = open(OUTPUT_FILE, "w")
for idx, label in enumerate(labels):
    # !!!!!!!!! Not sure if the label can be the actual name due to labeling, so I try with idx name
    # fout.write("\nitem { \n\tid: " + str(idx) + "\n\tname: '" + str(label) + "'\n}")
    # print("\nitem { \n\tid: " + str(idx) + "\n\tname: '" + str(label) + "'\n}")
    toWrite = "\nitem { \n\tid: " + str(idx + 1) + "\n\tname: '" + str(idx) + "'\n}"
    if idx != len(labels) - 1:
        toWrite += "\n"
    fout.write(toWrite)

