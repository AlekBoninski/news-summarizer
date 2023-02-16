class SummaryBuilder:

    def __init__(self, sentence_length):
        self.sentence_length = sentence_length
        self.last_sentence = None
        self.length = 0

    def add_sentence(self, sentence, score):
        if (self.length < self.sentence_length):
            if self.last_sentence is None:
                self.last_sentence = SentenceNode(sentence, score)
            else:
                self.last_sentence.next = SentenceNode(sentence, score)
                self.last_sentence.next.previous = self.last_sentence
                self.last_sentence = self.last_sentence.next
            self.length += 1
        else:
            self.__handle_add_new_sentence(sentence, score)

        return self

    def build(self):
        sentence_list = []
        current_sentence = self.last_sentence
        while current_sentence is not None:
            sentence_list = [current_sentence.text] + sentence_list
            current_sentence = current_sentence.previous
        return ' '.join(sentence_list)

    def __handle_add_new_sentence(self, sentence, score):
        lowest_score_node = self.__get_lowest_score_node()

        if lowest_score_node.score < score:
            if lowest_score_node.previous is not None:
                lowest_score_node.previous.next = lowest_score_node.next
            if lowest_score_node.next is not None:
                lowest_score_node.next.previous = lowest_score_node.previous
            if lowest_score_node.text == self.last_sentence.text:
                self.last_sentence = lowest_score_node.previous

            if self.last_sentence is None:
                self.last_sentence = SentenceNode(sentence, score)
            else:
                self.last_sentence.next = SentenceNode(sentence, score)
                self.last_sentence.next.previous = self.last_sentence
                self.last_sentence = self.last_sentence.next

    def __get_lowest_score_node(self):
        current_sentence = self.last_sentence
        lowest_score_node = None
        while current_sentence is not None:
            if lowest_score_node is None:
                lowest_score_node = current_sentence
            elif lowest_score_node.score >= current_sentence.score:
                lowest_score_node = current_sentence
            current_sentence = current_sentence.previous

        return lowest_score_node

class SentenceNode:
    
    def __init__(self, text, score):
        self.text = text
        self.score = score
        self.next = None
        self.previous = None
