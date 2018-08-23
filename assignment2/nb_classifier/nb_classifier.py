
import sys
import codecs
import math
import time
from html.parser import HTMLParser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer


tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
wnl = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        '''

        V dtype list[]
        ham dtype list[]
        spam dtype list[]
        file_names dtype list[] contains all files name

        '''

        self.V = []
        self.v_count = {}
        self.stops = []
        self.file_names = {}
        self.ham = []
        self.spam = []
        self.ham_files = set()
        self.spam_files = set()
        self.spam_count = 0
        self.ham_count = 0
        self.is_spam = 1


    def get_file_names(self):
        return self.file_names


    def get_stops(self):
        return self.stops
    

    def get_files_set(self):
        return self.spam_files,self.ham_files


    def get_v_count(self):
        return self.v_count


    def read_index_file(self,path):

        index_path = path + "/index"
        ifp = open(index_path,"r") # read index file

        for line in ifp: # read each line. ex : 'spam' 'inmail.12000'
            line = line.split()

            if line[0] == "spam":
                self.is_spam = 1
                self.spam_files.add(line[1].split('.')[-1])
                self.spam_count += 1

                fp = codecs.open(path+"/"+line[1],'r',encoding='utf-8',errors = 'ignore' )
                self.feed(fp.read())

                stop = len(self.V)
                self.stops.append(stop)
                self.file_names[stop] = line[1].split('.')[-1]

            elif line[0] == "ham":
                self.is_spam = 0
                self.ham_count += 1
                self.ham_files.add(line[1].split('.')[-1])

                fp = codecs.open(path+"/"+line[1],'r',encoding='utf-8',errors = 'ignore' )
                self.feed(fp.read())

                stop = len(self.V)
                self.stops.append(stop)
                self.file_names[stop] = line[1].split('.')[-1]
        self.stops.append(len(self.V))

        return self.V,self.ham,self.spam,self.ham_count,self.spam_count # ham/spam_count is the num of ham/spam file,   


    def handle_data(self, data): # overwrite handle_data
        data_list = tokenizer.tokenize(data)
        for each_data in data_list:
            lower_word = each_data.lower()
            if lower_word not in stop_words:
                lema_word = wnl.lemmatize(lower_word)
                self.V.append(lema_word)
                if self.is_spam :
                    self.spam.append(lema_word)
                    try:
                        self.v_count[lema_word,'spam'] += 1
                    except KeyError as e:
                        self.v_count[lema_word,'spam'] = 1
                else:
                    self.ham.append(lema_word)
                    try:
                        self.v_count[lema_word,'ham'] += 1
                    except KeyError as e:
                        self.v_count[lema_word,'ham'] = 1
        return True





def get_condition_prob(V,ham,spam,v_count,ham_count,spam_count,v_count_dict):

    file_count = spam_count + ham_count # total mail files count

    prior_spam = spam_count/file_count
    prior_ham =  ham_count/file_count

    condprob = {}   # condtional probability key is a word value is word's probability
    spam_denominator = 0
    ham_denominator = 0

    for v in V:
        try:
            spam_denominator += v_count_dict[v,'spam']+1
        except KeyError as e:
            spam_denominator += 1
        try:
            ham_denominator += v_count_dict[v,'ham']+1
        except KeyError as e:
            ham_denominator += 1

    for v in V:
        try:
            spam_numerator = v_count_dict[v,'spam']+1
        except KeyError as e:
            spam_numerator = 1
        try:
            ham_numerator =  v_count_dict[v,'ham']+1
        except KeyError as e:
            ham_numerator = 1
            
        condprob[(v,'spam')] = (1.0)*spam_numerator/spam_denominator
        condprob[(v,'ham')] = (1.0)*ham_numerator/ham_denominator

    return condprob,prior_spam,prior_ham


def apply_multinomial_nb( V, W,w_stops,w_index ,prior_spam, prior_ham, condprob):
    spam_result = set()
    ham_result = set()
    score_spam = math.log(prior_spam)
    score_ham = math.log(prior_ham)

    begin = 0
    for end in w_stops:
        for item in W[begin:end]:
            try:
                score_spam += math.log(condprob[item,'spam'])
                score_ham += math.log(condprob[item,'ham'])
            except Exception as e:
                continue
        if score_ham >= score_spam:
            ham_result.add(w_index[end])
        else:
            spam_result.add(w_index[end])
        begin = end
    return (spam_result, ham_result)




def get_accuracy(spam_result,ham_result,test_spam_set,test_ham_set):

    '''
    test_spam_set
        dtype:set contains the spam file_nams judged by index file

    test_ham_set
        dtype:set contains the ham file_nams judged by index file

    spam_result 
        dtype:set() contains the spam file_names judged by program 

    ham_result 
        dtype:set() contains the ham file_names judged by program 
    
    accuray
        rtype:float the result accuracy 
    '''


    t_p = len(test_spam_set.intersection(spam_result))
    f_p = len(spam_result) - t_p
    t_n = len(test_spam_set) - t_p
    f_n = len(test_spam_set)+len(test_ham_set) - t_p - f_p - t_n
    accuracy = (t_p+t_n)/(t_p + f_p + f_n + t_n)

    return accuracy


def check_argv():
    if len(sys.argv) != 3:
        return False
    else:
        return True


def main():
    # read command line
    if not check_argv():
        print("command line error.\npython3 nb_classifier.py [train_path] [test_path]")
        exit(1)


    # get train path and test path
    train_path = sys.argv[1]
    test_path = sys.argv[2]
    # init my_p my parser
    my_train = MyHTMLParser()
    my_test = MyHTMLParser()
    # get V, train_spam, train_ham, set of V 
    (V,train_ham,train_spam,train_ham_count,train_spam_count) = my_train.read_index_file(train_path) 
    V_set =set(V) 
    v_count = len(V_set)
    v_count_dict = my_train.get_v_count()


    # get train condition probability
    (condprob,prior_spam,prior_ham) = get_condition_prob(V_set,train_ham,train_spam,v_count,train_ham_count,train_spam_count,v_count_dict)



    # first we test train files
    # v_index contains all file_names = {....}
    v_index = my_train.get_file_names()
    v_stops = my_train.get_stops()
    (test_spam_set,test_ham_set) = my_train.get_files_set()

    (test_train_spam_result,test_train_ham_result) = apply_multinomial_nb( V_set, V,v_stops,v_index ,prior_spam, prior_ham, condprob)
    test_train_accuracy = get_accuracy(test_train_spam_result,test_train_ham_result,test_spam_set,test_ham_set)

    print("Training Accuracy: ",test_train_accuracy)



    # then we test test files
    (W,test_ham,test_spam,test_ham_count,test_spam_count) = my_test.read_index_file(test_path)
    w_index = my_test.get_file_names()
    w_stops = my_test.get_stops()
    (test_spam_set,test_ham_set) = my_test.get_files_set()

    (test_test_spam_result,test_test_ham_result) = apply_multinomial_nb( V_set, W,w_stops ,w_index ,prior_spam, prior_ham, condprob)
    test_test_accuracy = get_accuracy(test_test_spam_result,test_test_ham_result,test_spam_set,test_ham_set)

    print("Testing Accuracy: ",test_test_accuracy)



if __name__ == "__main__":
	main()