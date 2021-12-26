import csv


def getFirstName(name):
    name = name.lower().strip()
    index = name.find(' ')
    if index != -1:
        return name[:index]
    return name


def process_all_members(member_file, infile, outfile):
    with open(member_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        member_dict = {}
        member_dict_partial = {}
        for line in csv_reader:
            if line['TBC Member Record Type'] == "TBC Parent":
                continue
            member_dict[line['First Name'].lower().strip() + ":" + line['Last Name'].lower().strip() + ":" + line[
                'Email'].lower().strip()] = line
            member_dict_partial[line['First Name'].lower().strip() + ":" + line['Last Name'].lower().strip()] = line
        # print(member_dict)
    lines_processed = 0
    mismatched = 0
    corrected_match = 0
    with open(infile, "r") as csv_in:
        with open(outfile, "w", newline='') as csv_out:
            csv_reader = csv.DictReader(csv_in, delimiter=',')
            start_write = False

            for line in csv_reader:
                if not start_write:
                    line["TBC Member ID"] = ""
                    csv_writer = csv.DictWriter(csv_out, line.keys())
                    csv_writer.writeheader()
                    start_write = True
                index = line['First Name'].lower().strip() + ":" + line['Last Name'].lower().strip() + ":" + line[
                    'Email'].lower().strip()
                index2 = line['First Name'].lower().strip() + ":" + line['Last Name'].lower().strip()
                if index in member_dict:
                    line['TBC Member ID'] = member_dict[index]['TBC Member ID']
                elif index2 in member_dict_partial:
                    dict_item = member_dict_partial[index2]
                    if (((line['Parent 1 First Name'].lower().strip() == ""
                          or dict_item['Parent 1 First Name'].lower().strip() == ""
                          or line['Parent 1 First Name'].lower().strip() == getFirstName(
                                dict_item['Parent 1 First Name'])
                          or line['Parent 2 First Name'].lower().strip() == getFirstName(
                                dict_item['Parent 2 First Name'])
                          or line['Parent 1 First Name'].lower().strip() == getFirstName(
                                dict_item['Parent 2 First Name'])
                          or line['Parent 2 First Name'].lower().strip() == getFirstName(
                                dict_item['Parent 1 First Name']))
                         or line['Email'].lower().strip() == dict_item['Parent 1 Email'].lower().strip()
                         or line['Parent 1 Email'].lower().strip() == dict_item['Parent 1 Email'].lower().strip()
                         or line['Parent 1 Email'].lower().strip() == dict_item['Email'].lower().strip()
                         or line['Parent 1 Email'].lower().strip() == dict_item['Parent 2 Email'].lower().strip())):
                        #
                        # we are ok with the match
                        line['TBC Member ID'] = member_dict_partial[index2]['TBC Member ID']
                        corrected_match = corrected_match + 1
                    else:
                        print(index2)
                        mismatched = mismatched + 1
                csv_writer.writerow(line)
                lines_processed = lines_processed + 1
    print("Total records processed: " + str(lines_processed))
    print("Total records corrected: " + str(corrected_match))
    print("Total records mismatched: " + str(mismatched))


# tbcall.csv is dictionary file
# infile.csv is infile/ uploaded file
if __name__ == '__main__':
    process_all_members('C:\\tbc\\import\\tbcall.csv', 'C:\\tbc\\import\\infile.csv', 'C:\\tbc\\import\\outfile.csv')
