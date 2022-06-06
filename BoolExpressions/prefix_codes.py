def fano(probabilities: list):
    if sum(probabilities) != 1:
        raise ValueError('Sum of probabilities has to be equal 1')
    parts = [sorted(probabilities)[::-1]]
    codes = ['' for _ in parts[0]]
    stop = False
    print(end='| ')
    while not stop:
        stop = True
        new_parts = []
        new_codes = []
        for part in parts:
            if len(part) == 1:
                print(' ' * len(str(part[0])), end=' | ')
                new_parts += [part]
                new_codes += [codes.pop(0)]
                continue
            stop = False
            best_idx = -1
            best_diff = 1
            for idx in range(1, len(part)):
                diff = sum(part[:idx]) - (sum(part) / 2)
                if abs(diff) < best_diff:
                    best_idx = idx
                    best_diff = abs(diff)
            for idx in range(len(part)):
                cur_code = codes.pop(0)
                if idx < best_idx:
                    cur_code += '0'
                else:
                    cur_code += '1'
                new_codes += [cur_code]
            new_parts.append(part[:best_idx])
            new_parts.append(part[best_idx:])
            print('   '.join(map(str, part[:best_idx])), end=' | ')
            print('   '.join(map(str, part[best_idx:])), end=' | ')
        print(end='\n| ')
        parts = new_parts
        codes = new_codes
    average_length = 0
    for idx, probability in enumerate(parts):
        print(f'{codes[idx]:>{len(str(probability[0]))}}', end=' | ')
        average_length += len(codes[idx]) * probability[0]
    print(f'\n{average_length}\n')


def huffman(probabilities: list):
    if sum(probabilities) != 1:
        raise ValueError('Sum of probabilities has to be equal 1')

    def recurse(lst: list):
        if len(lst) <= 1:
            raise ValueError('List have to be at least 2 length')
        if len(lst) == 2:
            return ['0', '1']
        main, last = lst[:-2], lst[-2:]
        last_sum = last[0] + last[1]
        main.append(last_sum)
        probs = sorted(main)[::-1]
        returned_codes = recurse(probs)
        last_sum_idx = len(probs) - 1 - probs[::-1].index(last_sum)
        last_sum_code = returned_codes[last_sum_idx]
        returned_codes.pop(last_sum_idx)
        returned_codes.append(last_sum_code + '0')
        returned_codes.append(last_sum_code + '1')
        return returned_codes

    codes = recurse(sorted(probabilities)[::-1])
    average_length = 0
    print('  '.join(map(str, probabilities)))
    for idx, probability in enumerate(probabilities):
        print(f'{codes[idx]:>{len(str(probability))}}', end='  ')
        average_length += len(codes[idx]) * probability
    print('\n')
    print(round(average_length,
                max(map(lambda x: len(str(x)) - 1, probabilities))))
