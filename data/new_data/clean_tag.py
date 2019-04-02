import pickle
import os

tags = pickle.load(open('../agmir_data/unique_tag_list.pkl','rb'))


if __name__ == '__main__':
    f = open('../agmir_data/data_ordered_dict.pkl', 'rb')
    data = pickle.load(f)

    print(len(tags))

    num = 0

    with open('../agmir_data/train_data_list.txt', 'r') as input:
        with open('../agmir_data/train__data_sample.txt', 'w') as output:
            for each in input.readlines():
                key = each.strip()
                value = data['{}.png'.format(key)][-1]
                output.write(key)
                for tag in value:
                    if tag not in tags:
                        value.append('others')
                for tag in tags:
                    if tag in value:
                        num += 1
                        output.write(' 1')
                    else:
                        output.write(' 0')
                output.write('\n')
    print(num)
