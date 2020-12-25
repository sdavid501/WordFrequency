from mrjob.job import MRJob
from mrjob.step import MRStep
# -*- coding: utf-8 -*-

class MRWordFreq(MRJob):
    '''count word frequency'''

    def configure_args(self):
        super(MRWordFreq, self).configure_args()
        self.add_file_arg('--name', help='Path to 100KWikiText.txt')

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper1,
                reducer = self.reducer1),
            MRStep(mapper=self.mapper2,
                   reducer = self.reducer2)
        ]

    def mapper1(self, _, line):
        line = line.lower()
        words = line.split(' ')
        for i in range(len(words)):
            if any(c.isalpha() for c in words[i]):
                word = ''.join(e for e in words[i] if e.isalpha())
                if not word: continue  
                begin = 0
                if i > 1:
                    begin = i - 1
                end = i + 1
                if i + 1 >= len(words):
                    end = len(words) - 1
                
                for j in range(begin, end+1):
                    if i == j: continue
                    if any(c.isalpha() for c in words[j]):
                        adj = ''.join(e for e in words[j] if e.isalpha())
                        yield str(word) + ' ' + str(adj), 1.0
                yield str(word), (end - begin)

    def reducer1(self, key, values):
        yield key, sum(values)

    def mapper2(self, key, value):
        yield None, [key, value]

    def reducer2(self, key, values):
        dwords = {}
        swords = {}
        for i in values:
            if (len(i[0].split(' ')) == 2):
                dwords.update({i[0]: i[1]})
            else:
                swords.update({i[0]: i[1]})
        
        for i in dwords:
            dwords[i] = dwords[i]/swords[i.split(' ')[0]]

        s_words = dict(sorted(dwords.items(), key=lambda item: item[1], reverse=True))
        count = 0
        for i in s_words:
            if s_words[i] == 1.0: continue
            yield i, s_words[i]
            count = count + 1
            if count == 100: break


if __name__ == '__main__':
    MRWordFreq.run()
